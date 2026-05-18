# AI Policy & Product Helper

**RAG system** for policy and product questions using **FastAPI**, **Next.js**, and **Qdrant**.  
Supports document ingestion, question-answering with **citations**, metrics, health checks, and a minimal chat/admin UI.

---

## Features

- Ingest policy/product documents (Markdown, PDF, etc.)  
- RAG-based question answering with chunk-level citations  
- Built-in embeddings  
- OpenAI integration for real LLM answers  
- Metrics & health endpoints for observability  
- Minimal responsive chat UI with citation expansion  
- Fully containerized via Docker Compose

---

## Quick Start (Docker)

## 1. Set up your OpenAI api key in .env
```
OPENAI_API_KEY=sk-xxxxx
```
If your api key is invalid, try generate a new one.

## 2. Run all services:
   
```bash
docker compose up --build
```

if that did not work

try:
```bash
docker compose build --no-cache
```
and then:
```bash
docker compose up
```
-Frontend: http://localhost:3000

-Backend (Swagger docs): http://localhost:8000/docs

-Qdrant UI: http://localhost:6333/dashboard

## 3. Ingest sample docs:
```bash
curl -X POST http://localhost:8000/api/ingest
```
or via Admin panel in the UI.

## 4. Architecture

```bash
Frontend (Next.js)
 ├─ /app/page.tsx           # Chat UI
 ├─ /components/Chat.tsx
 └─ /components/AdminPanel.tsx

Backend (FastAPI)
 ├─ main.py                 # API endpoints
 ├─ rag.py                  # embeddings + retrieval + generation
 ├─ ingest.py               # document loader & chunker
 ├─ models.py               # Pydantic schemas
 └─ settings.py             # Environment & config

Vector DB: Qdrant (Docker)
 └─ Stores embeddings & chunks
```

## 5. Notes & Trade-offs

- **Embedding function**  
  The embed function generates a deterministic, local embedding for any text without using an external model.

  **Trade-offs:**  
  - Offline & deterministic: No external API needed.  
  - Works for any language or text, even unseen words.  

  **Limitations:**  
  - Very basic semantic understanding: only captures character patterns, not meaning.  
  - Fixed dimensionality can cause collisions when many n-grams map to the same index.  
  - Not suitable for large-scale, high-accuracy embeddings compared to OpenAI or HuggingFace models.  

- **Docker Compose** provides reproducibility.  

- **UI & metrics** are minimal, can be improved further.

## 6. Next Steps / What I’d Ship Next

- **Streaming answers**: Show partial responses in the UI for better user experience.  
- **File uploads**: Allow users to upload new policy/product documents with type validation.  
- **Frontend UX polish**: Better loading states, error handling, responsive design, and accessibility.  
- **Performance optimization**: Cache frequent queries, reduce latency, and monitor metrics.

## 7. Video Demo
[![Watch demo](https://img.youtube.com/vi/RboaGKO-E3A/maxresdefault.jpg)](https://youtu.be/RboaGKO-E3A)
