"""LLM extracts structured facts from one chunk. Groq JSON mode."""
import json
from backend.utils.llm import generate

_PROMPT = """You extract facts from a consulting company's document.

Read the text and return ONLY JSON with these keys (skip empty arrays):

{{
  "people": [{{"name": "..."}}],
  "clients": [{{"name": "...", "industry": "..."}}],
  "projects": [{{"name": "...", "type": "..."}}],
  "skills": ["..."],
  "decisions": [{{"text": "...", "reason": "...", "decided_by": "...", "status": "accepted"}}],
  "problems": [{{"text": "...", "severity": "low|medium|high"}}],
  "solutions": [{{"text": "...", "applied_by": "..."}}],
  "relationships": [{{"type": "WORKED_ON|HAD_PROBLEM|SOLVED|DECIDED|FOR_CLIENT", "from": "name", "to": "name"}}],
  "confidence": 0.0
}}

Text:
\"\"\"
{text}
\"\"\"
"""


def extract_facts(text: str) -> dict:
    """Return dict of extracted facts, or {confidence: 0} on failure."""
    raw = generate(_PROMPT.format(text=text[:4000]), json_mode=True, temperature=0.1)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"confidence": 0.0}