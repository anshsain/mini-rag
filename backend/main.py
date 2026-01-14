from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient

# ---------------------------
# App setup
# ---------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Request / Response models
# ---------------------------
class IngestRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

# ---------------------------
# Qdrant + Embeddings
# ---------------------------
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Qdrant(
    client=client,
    collection_name="mini_rag_docs",
    embeddings=embeddings,
)

# ---------------------------
# Gemini LLM
# ---------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def health():
    return {"status": "Backend is running"}

@app.post("/ingest")
def ingest(req: IngestRequest):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    docs = splitter.create_documents([req.text])
    vectorstore.add_documents(docs)

    return {
        "status": "Document ingested",
        "chunks": len(docs)
    }

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    docs = vectorstore.similarity_search(req.question, k=3)

    if not docs:
        return {"answer": "I could not find an answer in the provided document."}

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
Use ONLY the context below to answer the question.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{req.question}
"""

    response = llm.invoke(prompt)
    return {"answer": response.content}
