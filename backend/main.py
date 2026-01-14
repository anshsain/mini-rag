from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "Backend is running"}

@app.post("/query")
def query(req: QueryRequest):
    return {
        "answer": f"You asked: '{req.question}'. RAG logic will go here."
    }
