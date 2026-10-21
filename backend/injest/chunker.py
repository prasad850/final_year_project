def chunk_text(text : str, chunk_size: int = 500, overlap: int = 50):
    words = text.split()   # Split the text into words
    chunks=[]
    i=0
    while i< len(words):
        chunk = " ".join(words[i:i+chunk_size]) # join the single words into a string
        chunks.append(chunk)
        i+=chunk_size-overlap      #500-50 =450     then 450 + 500 -50 = 900
    return chunks

def chunk_documents(doc: dict):
    chunks= chunk_text(doc["text"])
    return[
        {
            "text": c, "source": doc["path"], "chunk_index": i
        }
        for i , c in enumerate(chunks)  
    ]

if __name__ =="__main__":
    from backend.injest.loader import load_documents
    docs = load_documents()
    total=0
    for d in docs:
        chunks =chunk_documents(d)
        total+=len(chunks)
        print(f"{d['path']}: {len(chunks)} chunks")
    print(f"Total chunks: {total}") 