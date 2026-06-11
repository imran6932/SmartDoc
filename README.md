# 📄 SmartDoc — AI Document Q&A

SmartDoc is an AI-powered document assistant that lets you upload PDF, DOCX, or TXT files and ask questions in natural language. Built with FastAPI, LangChain, OpenAI, and React.

## 🚀 Live Demo

- **Frontend**: [smartdoc.imranansari.in](https://smartdoc.imranansari.in)
- **API Docs**: [api.smartdoc.imranansari.in/docs](https://api.smartdoc.imranansari.in/docs)

---

## ✨ Features

- 📁 Upload PDF, DOCX, and TXT files (max 2MB)
- 🤖 Ask questions in natural language
- 🧠 Smart context detection — uses RAG for specific questions, full document for broad questions (summarize, review, describe)
- 💬 Multi-turn chat history per session
- 🔒 IP-based rate limiting — 3 uploads and 12 questions per day
- 🐳 Dockerized for easy deployment
- ⚡ Redis-backed rate limiting with auto daily reset

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| FastAPI | REST API framework |
| LangChain | RAG pipeline and LLM orchestration |
| OpenAI GPT-4o-mini | Language model for Q&A |
| OpenAI text-embedding-3-small | Document embeddings |
| FAISS | Vector store for semantic search |
| Redis | Rate limiting storage |
| Docker | Containerization |

### Frontend
| Technology | Purpose |
|---|---|
| React + Vite | UI framework |
| Axios | HTTP client |
| React Markdown | Markdown rendering |

---

## 🏗️ Architecture

```
User uploads file
      ↓
Text extracted (PDF / DOCX / TXT)
      ↓
Text chunked → Embeddings generated → Stored in FAISS
      ↓
User asks question
      ↓
Smart routing:
  Specific question → RAG (top 4 relevant chunks)
  Broad question    → Full document context
      ↓
GPT-4o-mini generates answer
      ↓
Response shown in chat UI
```

---

## 📁 Project Structure

```
smartdoc/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── limiter.py              # Redis rate limiting
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── routers/
│   │   ├── upload.py           # File upload endpoint
│   │   └── chat.py             # Q&A endpoint
│   └── services/
│       ├── extractor.py        # PDF / DOCX / TXT parser
│       ├── embedder.py         # Chunking + FAISS vector store
│       └── rag.py              # LangChain RAG chain
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── components/
│   │       ├── Uploader.jsx    # File upload UI
│   │       └── ChatBox.jsx     # Chat interface
│   └── .env.example
|── docker-compose.yml
|
|__ makefile
```

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Redis
- OpenAI API key

### Backend

```bash
cd backend

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your OPENAI_API_KEY in .env

# Run server
uvicorn main:app --reload
```

Backend runs at `http://127.0.0.1:8000`
API docs at `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Set VITE_API_URL=http://127.0.0.1:8000

# Run dev server
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## 🐳 Docker Setup

```bash
# Start all services
docker-compose up -d

# View logs
docker logs smartdoc-backend

# Stop all services
docker-compose down
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/api/upload` | Upload a document |
| POST | `/api/chat` | Ask a question |
| POST | `/api/clear` | Clear session history |

### Upload a file
```bash
curl -X POST https://api.smartdoc.imranansari.in/api/upload \
  -F "file=@document.pdf"
```

Response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "document.pdf",
  "message": "File uploaded and processed successfully"
}
```

### Ask a question
```bash
curl -X POST https://api.smartdoc.imranansari.in/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "question": "What is this document about?"
  }'
```

Response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "What is this document about?",
  "answer": "..."
}
```

---

## 🔒 Rate Limits

| Action | Limit |
|---|---|
| File uploads | 3 per day per IP |
| Questions | 12 per day per IP |

Limits reset automatically every 24 hours.

---

## 🌍 Environment Variables

### Backend `.env`
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Frontend `.env`
```env
VITE_API_URL=http://127.0.0.1:8000
```

---

## 👨‍💻 Author

**Imran Ansari**
- Portfolio: [imranansari.in](https://imranansari.in)
- Blog: [blog.imranansari.in](https://blog.imranansari.in)
- GitHub: [github.com/imranansari](https://github.com/imranansari)

---

## 📄 License

MIT License — feel free to use this project for learning or portfolio purposes.
