from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from services.rag import ask_question, clear_session
from limiter import check_limit

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    question: str


class ClearRequest(BaseModel):
    session_id: str


@router.post("/chat")
async def chat(request: Request, chat_request: ChatRequest):
    check_limit(request.client.host, "chats")
    if not chat_request.session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    if not chat_request.question:
        raise HTTPException(status_code=400, detail="question is required")

    try:
        answer = ask_question(chat_request.session_id, chat_request.question)
        return {
            "session_id": chat_request.session_id,
            "question": chat_request.question,
            "answer": answer,
        }
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail="Session not found. Please upload a document first."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear")
async def clear(request: ClearRequest):
    clear_session(request.session_id)
    return {"message": "Session cleared successfully"}
