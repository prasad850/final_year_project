from backend.injest.vector_store import search

def retrieve(query: str, n:int =10)-> list[dict]:
    """Return a list of {text, source, distance} for the top n documents."""
    return search(query, n)