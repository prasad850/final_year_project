"""LangGraph state — the data that flows through the graph."""
from typing import TypedDict, Optional


class AgentState(TypedDict):
    question: str                     # user's question
    answer: Optional[str]             # generated answer (if confident)
    citations: list[dict]             # sources
    confidence: float                 # 0.0-1.0
    decision: str                     # "answer" | "escalate" | "save"
    expert: Optional[dict]            # suggested expert (if escalate)
    saved_to_memory: bool             # whether we saved to Chroma