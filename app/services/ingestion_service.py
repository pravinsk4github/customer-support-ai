from langchain_core.documents import Document
from sqlalchemy.orm import Session

from app.repositories.faq_repository import FAQRepository
from app.schemas import BaseFAQModel
from app.services.vector_service import VectorService

class IngestionService:
    def __init__(self, db: Session):
        self.repository = FAQRepository(db)
        self.vector_service = VectorService()

    def _faq_to_document(self, faq: BaseFAQModel) -> Document:
        content = (
            f"Question: {faq.question}\n"
            f"Answer: {faq.answer}\n"
            f"Category: {faq.category or 'general'}\n"
            f"tags: {faq.tags or ''}"            
        )

        metadata = {
            "faq_id": faq.id,
            "category": faq.category or "general",
            "tags": faq.tags or ""
        }

        return Document(page_content=content, metadata=metadata)

    def sync_faqs_to_vector_store(self) -> int:
        faqs = self.repository.get_all_active_faqs()
        documents = [self._faq_to_document(faq) for faq in faqs] 
        
        ## Later we can optimize incremental sync, but for now full resync is totally fine.
        self.vector_service.reset_collection()
        self.vector_service.add_documents(documents)

        return len(documents)
