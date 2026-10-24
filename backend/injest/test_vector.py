from backend.injest.loader import load_documents
from backend.injest.chunker import chunk_documents
from backend.injest.vector_store import add_chunks, search

for d in load_documents():
    add_chunks(chunk_documents(d))

print(search("ERP migration", n=3))