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
            if "chroma_db" in str(path):
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                
                # If it's a Slack file (a list of messages)
                if isinstance(data, list) and len(data) > 0 and "user" in data[0]:
                    transcript = ""
                    for msg in data:
                        transcript += f"{msg.get('user', 'unknown')}: {msg.get('text', '')}\n"
                    docs.append({
                        "path": str(path),
                        "type": "slack_transcript",
                        "text": transcript,
                    })
                else:
                    # Normal JSON
                    docs.append({
                        "path": str(path),
                        "type": "json",
                        "text": json.dumps(data, indent=2),
                    })
            except json.JSONDecodeError:
                continue

    return docs

if __name__ == "__main__":
    docs =load_documents()
    print(f"loaded {len(docs)} documents")
    for d in docs[:3]:
        print(f"{d['path']} ({d['type']})")