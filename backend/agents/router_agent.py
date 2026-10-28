# """LangGraph agent that decides answer / escalate / save."""
# from langgraph.graph import StateGraph, START, END
# from backend.graph.expert_finder import find_expert
# from backend.agents.state import AgentState
# from backend.rag.answerer import answer as rag_answer
# from backend.rag.confidence import assess
# from backend.rag.retriever import retrieve
# from backend.graph.queries import find_expert_by_keyword, find_expert_by_problem
# from backend.utils.llm import generate
# from backend.injest.vector_store import add_chunks
# from backend.injest.embeder import embed
# from backend.injest.vector_store import get_collection
# import time


# def classify_and_answer(state: AgentState) -> AgentState:
#     """Step 1: retrieve, assess, generate answer if confident."""
#     result = rag_answer(state["question"])
#     state["answer"] = result["answer"]
#     state["citations"] = result["citations"]
#     state["confidence"] = result["confidence"]

#     if result["escalate"]:
#         state["decision"] = "escalate"
#     else:
#         state["decision"] = "answer"

#     return state


# def route_by_decision(state: AgentState) -> str:
#     """Step 2: conditional edge — route based on state['decision']."""
#     return state["decision"]


# def escalate_node(state: AgentState) -> AgentState:
#     """Step 3a: find who might know the answer."""
#     # Extract 1-3 keywords from the question
#     # keywords_raw = generate(
#     #     f"Extract 1-3 technical keywords from this question. Comma-separated, no other text:\n{state['question']}",
#     #     temperature=0.0,
#     # )
#     # keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]

#     # expert = None
#     # for kw in keywords:
#     #     expert = find_expert_by_keyword(kw) or find_expert_by_problem(kw)
#     #     if expert:
#     #         break
#     expert = find_expert(state["question"])

#     state["expert"] = expert
#     state["answer"] = (
#         f"I don't have enough information. "
#         f"Suggested expert: {expert['name']}" if expert
#         else "I don't have enough information, and no expert found."
#     )
#     return state


# def save_node(state: AgentState) -> AgentState:
#     """Step 3b: save a human's answer to permanent memory."""
#     # In this flow, state["answer"] is the human-provided answer
#     col = get_collection()
#     text = state["answer"]
#     col.add(
#         embeddings=embed([text]),
#         documents=[text],
#         metadatas=[{"source": "human_answer"}],
#         ids=[f"saved_{int(time.time())}"],
#     )
#     state["saved_to_memory"] = True
#     return state


# def build_agent():
#     """Wire up the LangGraph."""
#     graph = StateGraph(AgentState)

#     graph.add_node("classify", classify_and_answer)
#     graph.add_node("escalate", escalate_node)
#     graph.add_node("save", save_node)

#     graph.add_edge(START, "classify")

#     # Conditional routing after classify
#     graph.add_conditional_edges(
#         "classify",
#         route_by_decision,
#         {
#             "answer": END,
#             "escalate": "escalate",
#         },
#     )

#     graph.add_edge("escalate", END)
#     graph.add_edge("save", END)

#     return graph.compile()


# _agent = None


# def get_agent():
#     global _agent
#     if _agent is None:
#         _agent = build_agent()
#     return _agent


# def run_agent(question: str) -> AgentState:
#     """Entry point: run the graph from START."""
#     initial: AgentState = {
#         "question": question,
#         "answer": None,
#         "citations": [],
#         "confidence": 0.0,
#         "decision": "",
#         "expert": None,
#         "saved_to_memory": False,
#     }
#     return get_agent().invoke(initial)


from backend.graph.neo4j_client import run_query
from backend.agents.state import AgentState
from backend.rag.answerer import answer as rag_answer
from backend.utils.llm import generate
import json

def find_expert(question: str) -> dict:
    """Extract keywords from the question, then find the best person in Neo4j."""
    
    # 1. Ask the LLM to extract keywords (Strict JSON Object for Groq)
    prompt = f"""Extract 1 to 3 technical keywords from this question. 
    Return ONLY a JSON object with a single key "keywords" containing an array of strings. 
    Example: {{"keywords": ["AWS", "ERP"]}}
    
    Question: {question}"""
    
    try:
        raw = generate(prompt, json_mode=True, temperature=0.0)
        data = json.loads(raw)
        keywords = data.get("keywords", [])
        if not keywords:
             raise ValueError("No keywords found")
    except Exception as e:
        print(f"LLM keyword extraction failed: {e}. Falling back to basic words.")
        # Fallback: just use the longest words in the question
        keywords = [word for word in question.split() if len(word) > 4][:3]

    # 2. Query Neo4j (Removed the illegal [..3] slice)
    cypher = """
        MATCH (p:Person)-[r:HAS_SKILL|WORKED_ON|DECIDED|SOLVED]->(n)
        WHERE any(keyword IN $keywords WHERE 
            toLower(coalesce(n.name, n.text, "")) CONTAINS toLower(keyword)
        )
        RETURN p.name AS expert_name, count(r) AS score, collect(DISTINCT coalesce(n.name, n.text)) AS matched_topics
        ORDER BY score DESC
        LIMIT 1
    """
    
    results = run_query(cypher, keywords=keywords)
    
    if results:
        best_match = results[0]
        # Slice the list safely in Python
        topics_list = best_match["matched_topics"]
        topics = ", ".join(topics_list[:3]) if topics_list else "related topics"
        return {
            "name": best_match["expert_name"],
            "reason": f"has worked on {topics}"
        }
    
    return None


def run_agent(question: str) -> AgentState:
    """Run the current RAG flow and enrich escalated answers with an expert."""
    result = rag_answer(question)
    decision = "escalate" if result["escalate"] else "answer"
    expert = find_expert(question) if result["escalate"] else None

    return {
        "question": question,
        "answer": result["answer"],
        "citations": result["citations"],
        "confidence": result["confidence"],
        "decision": decision,
        "expert": expert,
        "saved_to_memory": False,
    }