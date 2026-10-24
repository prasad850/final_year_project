"""Answer generation — plain Python, no LCEL chains."""
from backend.rag.retriever import retrieve
from backend.rag.confidence import assess
from backend.utils.llm import generate


def answer(question: str) -> dict:
    """Full RAG: retrieve, assess, generate, return structured dict."""
    results = retrieve(question, top_k=5)
    assessment = assess(question, results)

    if assessment["escalate"]:
        return {
            "answer": "I don't have enough information to answer.",
            "citations": [],
            "confidence": assessment["confidence"],
            "escalate": True,
            "reason": assessment["reason"],
        }

    context = "\n\n---\n\n".join(r["text"] for r in results)
    prompt = f"""Answer using ONLY the context below. If the context
does not contain the answer, say "I don't know."

Context:
{context}

Question: {question}

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