"""Ingest all documents into Chroma and Neo4j with provenance."""
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
import os
print("KEY LOADED:", (os.getenv("GROQ_API_KEY") or "MISSING")[:12] + "...")
import time
from backend.injest.loader import load_documents
from backend.injest.chunker import chunk_documents
from backend.injest.vector_store import add_chunks
from backend.graph.extractor import extract_facts
from backend.graph.writer import write_document, write_extraction

SKIP_GRAPH_FOLDERS = {"hr"}


def should_extract_to_graph(path: str) -> bool:
    parts = Path(path).parts
    return "hr" not in parts


def _infer_team(path: str) -> str:
    parts = Path(path).parts
    if any(p in parts for p in ["proposals", "pricing", "clients", "case_studies"]):
        return "Pre-Sales"
    if "support" in parts:
        return "Support"
    if any(p in parts for p in ["slack", "delivery", "adr", "post_mortems"]):
        return "Delivery"
    return ""


def main():
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")

    for doc in docs:
        # 1. Write Document node (once per file)
        write_document(doc["path"], {
            "title": doc["path"].split("/")[-1],
            "type": doc["type"],
            "team": _infer_team(doc["path"]),
        })

        # 2. Chroma — always
        chunks = chunk_documents(doc)
        add_chunks(chunks)
        print(f"  {doc['path']}: {len(chunks)} chunks → Chroma")

        # 3. Neo4j — only for graph-worthy folders
        if not should_extract_to_graph(doc["path"]):
            continue
        for chunk in chunks:
            facts = extract_facts(chunk["text"])
            if facts.get("confidence", 0) >= 0.5:
                write_extraction(chunk["source"], facts)
            time.sleep(1.5)  # Groq free-tier rate limit

    print("Done.")


if __name__ == "__main__":
    main()