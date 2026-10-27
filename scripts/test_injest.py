# from backend.injest.loader import load_documents
# from backend.injest.chunker import chunk_documents
# from backend.injest.vector_store import add_chunks, search

# for d in load_documents():
#     add_chunks(chunk_documents(d))

# print(search("ERP migration", n=3))
from backend.injest.vector_store import search

q = "who decided to use AWS over Azure for ERP hosting"
results = search(q, n=5)

for r in results:
    print(f"distance={r['distance']:.4f}  source={r['source']}")
    print(f"  text: {r['text'][:120]}...")
    print()