# 🚀 Customer Support AI Chatbot (RAG-based)

A **production-style AI-powered customer support chatbot** built using FastAPI, LangChain, and Chroma, designed with real-world backend architecture principles.

This project demonstrates how to build a reliable AI system using **Retrieval-Augmented Generation (RAG)** with strong focus on **accuracy, observability, and clean architecture**.

---

## ✨ Key Features

- 🔍 **RAG-based retrieval** using vector embeddings (Chroma)
- 🎯 **Advanced retrieval logic**
  - Score threshold filtering (absolute relevance)
  - Score gap validation (confidence-based selection)
  - Top-1 document grounding for precise answers
- 💬 **Session-based conversational memory**
- 🧠 **FAQ-driven knowledge base** (SQLite as source of truth)
- ⚙️ **FastAPI backend with clean layered architecture**
- 🛡️ **Centralized exception handling**
- 📊 **Structured logging**
- 🔗 **Request tracing with request_id middleware**
- 🚫 **Safe fallback responses for low-confidence queries**

---

## 🧠 Architecture Overview

```
Client → FastAPI API → Service Layer → Repository Layer → SQLite (FAQs)
                               ↓
                         Vector Store (Chroma)
                               ↓
                           LLM (LangChain)
```

### Design Principles

- Separation of concerns (API / Services / Repositories)
- Production-style error handling
- Observability-first design (logging + tracing)
- Safe AI responses (no hallucination via retrieval checks)

---

## 🔍 How Retrieval Works

The system improves response accuracy using **multi-stage validation**:

1. Retrieve top-K documents from vector DB
2. Select best match using similarity score
3. Apply:
   - **Score Threshold** → ensures absolute relevance
   - **Score Gap** → ensures confidence vs second-best match
4. If conditions pass → use context  
5. Else → return fallback response

👉 This avoids hallucinations and improves reliability.

---

## 🛠️ Tech Stack

| Layer            | Technology |
|------------------|-----------|
| Backend API      | FastAPI |
| Language         | Python |
| AI Framework     | LangChain |
| Vector Database  | Chroma |
| Data Store       | SQLite |
| Embeddings       | OpenAI / compatible |
| Logging          | Python logging (structured) |
| Architecture     | Clean layered design |

---

## 📂 Project Structure

```
app/
 ├── api/                # FastAPI routes, middleware, exception handlers
 ├── services/           # Business logic (RAG pipeline)
 ├── repositories/       # Data access (SQLite)
 ├── core/               # Exceptions, request context
 ├── utils/              # Logger, helpers
 ├── rag/                # Retrieval logic, vector handling
```

---

## 🚀 Getting Started

### 1. Clone repo

```bash
git clone https://github.com/<your-username>/customer-support-ai.git
cd customer-support-ai
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # mac/linux
venv\Scripts\activate      # windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set environment variables

Create `.env` file:

```env
OPENAI_API_KEY=your_key_here
```

---

### 5. Run application

```bash
uvicorn app.main:app --reload
```

---

### 6. Test API

Open Swagger UI:

http://127.0.0.1:8000/docs

---

## 📡 Example API Request

```json
POST /chat

{
  "session_id": "user123",
  "message": "What is your refund policy?"
}
```

---

## 📦 Example Response

```json
{
  "answer": "You can request a refund within 30 days...",
  "sources": [
    {
      "document": "FAQ document",
      "page": 1
    }
  ]
}
```

---

## ❌ Error Handling Example

```json
{
  "error": {
    "code": "resource_not_found",
    "message": "No session found"
  },
  "request_id": "abc-123"
}
```

---

## 🔍 Observability

- Structured logs for debugging
- Request tracing via `request_id`
- Centralized exception handling
- Safe error responses (no internal leaks)

---

## 🧪 Testing

```bash
pytest
```

---

## 🚧 Future Improvements

- Docker support
- CI/CD pipeline
- Authentication & rate limiting
- Evaluation dataset for RAG accuracy
- Caching layer for responses

---

## 💡 Why this project?

This project is designed to showcase:

- Real-world AI system design
- Backend engineering best practices
- Clean architecture implementation
- Reliable and safe AI integration

---

## 👤 Author

**Praveen Kadam**

- Azure / Cloud Architect
- Backend Engineer
- AI Systems Builder

---

## ⭐ If you found this useful

Give it a ⭐ on GitHub!
