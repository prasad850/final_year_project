import chromadb
from backend.injest.embeder import embed

_client =None
_collection = None

def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path="data/chroma_db")
        _collection = _client.get_or_create_collection("documents")
    return _collection

def add_chunks(chunks: list[dict]):
    collection = get_collection()
    texts = [c["text"] for c in chunks]
    collection.add(
        embeddings=embed(texts),
        documents=texts,
        metadatas=[{"source": c["source"]} for c in chunks],
        ids = [f"{c["source"]}_{c["chunk_index"]}" for c in chunks]
    )

def search(query : str , n: int =5) -> list[dict]:
    col = get_collection()
    result = col.query(query_embeddings=embed(query), n_results=n)

    return[
        {"text": doc , "source":meta["source"], "distance": dist }
        for doc, meta, dist in zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
            )
    ]


