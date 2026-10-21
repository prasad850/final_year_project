from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app=FastAPI(title="memory agent")

@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/version")
def version():
    return{"version" : "1.0", "semister": "1"}

