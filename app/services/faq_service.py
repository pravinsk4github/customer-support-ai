from sqlalchemy.orm import Session
from app.core.exception import NotFoundError
from app.models import FAQ
from app.repositories.faq_repository import FAQRepository
from app.schemas import FAQCreate

class FAQService:
    def __init__(self, db: Session):
        self.repository = FAQRepository(db)

    def create_faq(self, faq: FAQCreate) -> FAQ:
        return self.repository.create_faq(faq)
    
    def get_active_faqs(self) -> list[FAQ]:
        return self.repository.get_all_active_faqs()

    def get_faq_by_id(self, faq_id: int) -> FAQ | None:
        faq = self.repository.get_faq_by_id(faq_id=faq_id)
        if faq is None:
            raise NotFoundError("FAQ not found")
        return faq
