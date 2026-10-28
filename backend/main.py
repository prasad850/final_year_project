# """FastAPI — routes that call plain functions and the agent."""
# from fastapi import FastAPI
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from typing import Optional

# load_dotenv()

# from backend.rag.answerer import answer as rag_answer
# from backend.agents.router_agent import run_agent
# from backend.injest.vector_store import search, add_chunks
# from backend.injest.embeder import embed
# from backend.injest.vector_store import get_collection

# app = FastAPI(title="Nova Memory Agent")


# # --- Health ---
# @app.get("/health")
# def health():
#     return {"status": "ok"}


# # --- Ask (uses the LangGraph agent) ---
# class AskRequest(BaseModel):
#     question: str


# @app.post("/ask")
# def ask(req: AskRequest):
#     state = run_agent(req.question)
#     return {
#         "answer": state["answer"],
#         "citations": state["citations"],
#         "confidence": state["confidence"],
#         "escalate": state["decision"] == "escalate",
#         "expert": state["expert"],
#     }


# # --- Plain RAG (baseline for comparison) ---
# @app.post("/ask/plain")
# def ask_plain(req: AskRequest):
#     return rag_answer(req.question)


# # --- Save ---
# class SaveRequest(BaseModel):
#     question: str
#     answer: str
#     person: str


# @app.post("/save")
# def save(req: SaveRequest):
#     col = get_collection()
#     import time
#     col.add(
#         embeddings=embed([req.answer]),
#         documents=[req.answer],
#         metadatas=[{"source": f"human_answer_by_{req.person}"}],
#         ids=[f"saved_{int(time.time())}"],
#     )
#     return {"status": "saved"}


# # --- Search (for debugging) ---
# class SearchRequest(BaseModel):
#     query: str


# @app.post("/search")
# def search_endpoint(req: SearchRequest):
#     return {"results": search(req.query, n=5)}



"""FastAPI — routes that call plain functions and the agent."""
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional, List
import time

load_dotenv()

from backend.rag.answerer import answer as rag_answer
from backend.agents.router_agent import run_agent
from backend.injest.vector_store import search
from backend.injest.embeder import embed
from backend.injest.vector_store import get_collection

app = FastAPI(title="Nova Memory Agent")

@app.get("/health")
def health():
    return {"status": "ok"}

# --- Pydantic Models ---
class AskRequest(BaseModel):
    question: str
    role: str = "Employee" # Default

class Citation(BaseModel):
    source: str
    text: str

class Expert(BaseModel):
    name: str
    reason: str

class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: float
    escalate: bool
    expert: Optional[Expert] = None  # <-- Now Swagger knows about this!

class SaveRequest(BaseModel):
    question: str
    answer: str
    person: str

class SearchRequest(BaseModel):
    query: str

# --- Routes ---

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    """Main endpoint using the LangGraph Agent."""
    state = run_agent(req.question)
    return {
        "answer": state["answer"],
        "citations": state["citations"],
        "confidence": state["confidence"],
        "escalate": state["decision"] == "escalate",
        "expert": state["expert"],
    }

@app.post("/ask/plain")
def ask_plain(req: AskRequest):
    """Baseline endpoint using standard RAG only (no agent)."""
    return rag_answer(req.question)

@app.post("/save")
def save(req: SaveRequest):
    col = get_collection()
    col.add(
        embeddings=embed([req.answer]),
        documents=[req.answer],
        metadatas=[{"source": f"human_answer_by_{req.person}"}],
        ids=[f"saved_{int(time.time())}"],
    )
    return {"status": "saved"}

@app.post("/search")
def search_endpoint(req: SearchRequest):
    return {"results": search(req.query, n=5)}