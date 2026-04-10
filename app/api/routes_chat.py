from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", 
    response_model=ChatResponse,
    summary="AI customer support chatbot",
    description="Returns an AI-generated response using RAG with confidence validation"
)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    service = ChatService(db)
    result = service.ask(
        session_id=payload.session_id,
        user_message=payload.message
    )
    return result

