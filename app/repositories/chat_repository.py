from sqlalchemy.orm import Session
from app.models import ChatSession, ChatMessage
from app.schemas import ChatMessageCreate

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session_if_not_exists(self, session_id: str) -> None:
        existing = (
            self.db.query(ChatSession)
            .filter(ChatSession.session_id == session_id)
            .first()
        )

        if not existing:
            session = ChatSession(session_id=session_id)
            self.db.add(session)
            self.db.commit()

    def add_message(self, chatdata: ChatMessageCreate) -> ChatMessage:
        chat_message = ChatMessage(**chatdata.model_dump())
        self.db.add(chat_message)
        self.db.commit()
        self.db.refresh(chat_message)    

    def get_recent_messages(self, session_id: str, limit: int = 6) -> list[ChatMessage]:
        messages = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.id.desc())
            .limit(limit)
            .all()
        )

        return list(reversed(messages))
        