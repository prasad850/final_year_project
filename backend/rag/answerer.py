"""Answer generation — plain Python, no LCEL chains."""
from backend.rag.retriever import retrieve
from backend.rag.confidence import assess
from backend.utils.llm import generate



def answer(question: str) -> dict:
    """Full RAG: retrieve, assess, generate, return structured dict."""
    results = retrieve(question, n=15)
    assessment = assess(question, results)

    if assessment["escalate"]:
        # NEW: Find the expert before returning
        
        return {
            "answer": "I don't have enough information to answer.",
            "citations": [],
            "confidence": assessment["confidence"],
            "escalate": True,
            "reason": assessment["reason"],
            
        }

    context = "\n\n---\n\n".join(r["text"] for r in results)
    prompt = f"""You are answering questions about a consulting firm. Answer using ONLY the context below. If the context
does not contain the answer, say "I don't know." and also tell why this desision taken and who taken and because of what only answer from context "

Context:
{context}

Question: {question}
Rules:

- If the context answers part of the question, answer that part and state what is missing.
- Do not say "I don't know" unless the context is completely unrelated to the question.
- If the context mentions an author, decider, or person responsible, treat them as the answer to "who decided".
Answer:"""

    text = generate(prompt)
    citations = [
        {"source": r["source"], "text": r["text"][:200]}
        for r in results[:3]
    ]

    return {
        "answer": text,
        "citations": citations,
        "confidence": assessment["confidence"],
        "escalate": False,
        "reason": "ok",
    }