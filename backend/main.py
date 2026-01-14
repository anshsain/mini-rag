from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
