from pathlib import Path
import json

def load_documents(data_dir : str ="data"):
    docs =[]
    for path in Path(data_dir).rglob("*.md"):
        docs.append({
            "path": str(path),
            "type": "markdown",
            "text" : path.read_text(encoding="utf-8")
        })
    for path in Path(data_dir).rglob("*.json"):
        docs.append({
            "path": str(path),
            "type": "json",
            "text": path.read_text(encoding="utf-8")
        })
    return docs

if __name__ == "__main__":
    docs =load_documents()
    print(f"loaded {len(docs)} documents")
    for d in docs[:3]:
        print(f"{d['path']} ({d['type']})")