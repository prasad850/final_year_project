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

def search(query : str , n: int =5, role: str = "Employee") -> list[dict]:
    col = get_collection()
    if col.count() == 0:
        return []
    where_filter = None
    if role == "Guest":
        # Assuming we tag documents with {"is_public": True/False} during ingest
        # For now, we will do a basic filter on source path
        pass 
    result = col.query(
        query_embeddings=embed([query]), 
        n_results=n,
        # where=where_filter 
    )
    

    return[
        {"text": doc , "source":meta["source"], "distance": dist }
        for doc, meta, dist in zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
            )
    ]


