from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseFAQModel(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    tags: Optional[str] = None
    is_active: int = 1


class FAQCreate(BaseFAQModel):
    pass

class FAQResponse(BaseFAQModel):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_active: Optional[int] = None

class ChatMessageCreate(BaseModel):
    session_id: str
    role: str
    message: str

class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[dict]