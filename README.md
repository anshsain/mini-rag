# Mini RAG Application (LangChain + Qdrant)

This project is a minimal yet production-grade **Retrieval-Augmented Generation (RAG)** application built as part of a technical assessment.

The system allows users to:
- Ingest a text document
- Ask questions grounded in the document
- Receive answers with inline citations
- View the sources used for each answer

The focus of this project is **correct RAG architecture and clarity**, not UI polish.

---

## Live Demo

- **Frontend**: https://mini-rag-xi.vercel.app/
- **Backend**: https://mini-rag-backend-njdx.onrender.com/

---

## Architecture Overview
User
↓
Next.js Frontend
↓
FastAPI Backend
↓
Document Chunking (1000 tokens, 10% overlap)
↓
Embeddings (OpenAI)
↓
Vector Storage (Qdrant)
↓
Retrieval (Top-k semantic search)
↓
Reranking (Cohere)
↓
Answer Generation with citations


---

## Tech Stack

### Backend
- Python 3.10
- FastAPI
- LangChain
- OpenAI (Embeddings + LLM)
- Cohere (Reranking)
- Qdrant Cloud (Vector Database)

### Frontend
- Next.js (Pages Router)
- React
- Minimal UI for clarity

### Hosting
- Backend: Render
- Frontend: Vercel
- Vector DB: Qdrant Cloud

---

## Vector Database Configuration

- **Provider**: Qdrant Cloud
- **Collection Name**: `mini_rag_docs`
- **Embedding Dimension**: 1536
- **Distance Metric**: Cosine
- **Upsert Strategy**: Chunk-level upsert with unique IDs

### Stored Metadata
Each chunk is stored with:
- `text`
- `source`
- `chunk_id`
- `position`

This metadata is used for **source attribution and citations**.

---

## Chunking Strategy

- **Chunk Size**: 1000 tokens
- **Chunk Overlap**: 100 tokens
- **Splitter**: RecursiveCharacterTextSplitter

This balances semantic coherence with effective retrieval.

---

## Retrieval & Ranking

### Initial Retrieval
- **Strategy**: Top-k semantic similarity search
- **Top-k**: 10

### Reranking
- **Model**: Cohere Rerank
- **Top-n**: 5

Reranking improves answer precision before passing context to the LLM.

---

## Answer Generation

- **LLM**: OpenAI GPT-4 / GPT-3.5
- **Temperature**: Low (factual grounding)
- **Prompting Strategy**:
  - Use only retrieved context
  - If answer is not found, explicitly say so
  - Include inline citations
