from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import FAQCreate, FAQResponse
from app.services.faq_service import FAQService

router = APIRouter(prefix="/faqs", tags=["FAQs"])

@router.post("/", response_model=FAQResponse)
def create_faq(faq: FAQCreate, db: Session = Depends(get_db)):
    service = FAQService(db)
    return service.create_faq(faq)

@router.get("/", response_model=list[FAQResponse])
def list_faqs(db: Session = Depends(get_db)):
    service = FAQService(db)
    return service.get_active_faqs()
