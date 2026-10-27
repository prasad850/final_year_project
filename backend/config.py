import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")

CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "memory_agent"



LLM_MODEL = "openai/gpt-oss-120b"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chroma distances near 0.6 can still be relevant for short natural-language
# questions whose wording differs from the indexed document.
CONFIDENCE_DISTANCE_THRESHOLD = 1.2

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "123123123"