"""Read all .md and .json files under data/. Plain Python."""
import json
from pathlib import Path


def load_documents(data_dir: str = "data") -> list[dict]:
    """Return a list of {path, type, text} for every document."""
    docs = []

    for path in Path(data_dir).rglob("*.md"):
        docs.append({
            "path": str(path),
            "type": "markdown",
            "text": path.read_text(encoding="utf-8"),
        })

    for path in Path(data_dir).rglob("*.json"):
        # Skip the Chroma folder if it lives under data/
        if "chroma_db" in str(path):
            continue
        try:
            docs.append({
                "path": str(path),
                "type": "json",
                "text": json.dumps(json.loads(path.read_text(encoding="utf-8")), indent=2),
            })
        except json.JSONDecodeError:
            continue

    return docs

if __name__ == "__main__":
    docs =load_documents()
    print(f"loaded {len(docs)} documents")
    for d in docs[:3]:
        print(f"{d['path']} ({d['type']})")