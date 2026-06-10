from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag import ask_question, clear_session

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    question: str


class ClearRequest(BaseModel):
    session_id: str


@router.post("/chat")
async def chat(request: ChatRequest):
    if not request.session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    if not request.question:
        raise HTTPException(status_code=400, detail="question is required")

    try:
        answer = ask_question(request.session_id, request.question)
        return {
            "session_id": request.session_id,
            "question": request.question,
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
