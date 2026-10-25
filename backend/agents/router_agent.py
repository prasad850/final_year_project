"""LangGraph agent that decides answer / escalate / save."""
from langgraph.graph import StateGraph, START, END

from backend.agents.state import AgentState
from backend.rag.answerer import answer as rag_answer
from backend.rag.confidence import assess
from backend.rag.retriever import retrieve
from backend.graph.queries import find_expert_by_keyword, find_expert_by_problem
from backend.utils.llm import generate
from backend.ingest.vector_store import add_chunks
from backend.ingest.embedder import embed
from backend.ingest.vector_store import _get_collection
import time


def classify_and_answer(state: AgentState) -> AgentState:
    """Step 1: retrieve, assess, generate answer if confident."""
    result = rag_answer(state["question"])
    state["answer"] = result["answer"]
    state["citations"] = result["citations"]
    state["confidence"] = result["confidence"]

    if result["escalate"]:
        state["decision"] = "escalate"
    else:
        state["decision"] = "answer"

    return state


def route_by_decision(state: AgentState) -> str:
    """Step 2: conditional edge — route based on state['decision']."""
    return state["decision"]


def escalate_node(state: AgentState) -> AgentState:
    """Step 3a: find who might know the answer."""
    # Extract 1-3 keywords from the question
    keywords_raw = generate(
        f"Extract 1-3 technical keywords from this question. Comma-separated, no other text:\n{state['question']}",
        temperature=0.0,
    )
    keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]

    expert = None
    for kw in keywords:
        expert = find_expert_by_keyword(kw) or find_expert_by_problem(kw)
        if expert:
            break

    state["expert"] = expert
    state["answer"] = (
        f"I don't have enough information. "
        f"Suggested expert: {expert['name']}" if expert
        else "I don't have enough information, and no expert found."
    )
    return state


def save_node(state: AgentState) -> AgentState:
    """Step 3b: save a human's answer to permanent memory."""
    # In this flow, state["answer"] is the human-provided answer
    col = _get_collection()
    text = state["answer"]
    col.add(
        embeddings=embed([text]),
        documents=[text],
        metadatas=[{"source": "human_answer"}],
        ids=[f"saved_{int(time.time())}"],
    )
    state["saved_to_memory"] = True
    return state


def build_agent():
    """Wire up the LangGraph."""
    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_and_answer)
    graph.add_node("escalate", escalate_node)
    graph.add_node("save", save_node)

    graph.add_edge(START, "classify")

    # Conditional routing after classify
    graph.add_conditional_edges(
        "classify",
        route_by_decision,
        {
            "answer": END,
            "escalate": "escalate",
        },
    )

    graph.add_edge("escalate", END)
    graph.add_edge("save", END)

    return graph.compile()


_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent


def run_agent(question: str) -> AgentState:
    """Entry point: run the graph from START."""
    initial: AgentState = {
        "question": question,
        "answer": None,
        "citations": [],
        "confidence": 0.0,
        "decision": "",
        "expert": None,
        "saved_to_memory": False,
    }
    return get_agent().invoke(initial)