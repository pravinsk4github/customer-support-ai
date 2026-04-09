import sqlite3
from sqlalchemy.orm import Session
from app.core.exception import RepositoryError
from app.models import FAQ
from app.schemas import FAQCreate

class FAQRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_faq(self, faq_data: FAQCreate) -> FAQ:
        try:
            faq = FAQ(**faq_data.model_dump())
            self.db.add(faq)
            self.db.commit()
            self.db.refresh(faq)
            return faq
        except sqlite3.Error as exc:
            raise RepositoryError("Failed to add FAQ into database.") from exc

    
    def get_all_active_faqs(self) -> list[FAQ]:
        try:
            return(
                self.db.query(FAQ)
                .filter(FAQ.is_active == 1)
                .order_by(FAQ.id.asc())
                .all()
            )
        except Exception as exc:
            raise RepositoryError("Failed to fetch faqs from the databse.") from exc

    def get_faq_by_id(self, faq_id: int) -> FAQ | None:
        try:
            return self.db.query(FAQ).filter(FAQ.od == faq_id).first()
        except Exception as exc:
            raise RepositoryError("Failed to fetch faq form the database.") from exc

    def delete_all_faqs(self) -> None:
        try:
            self.db.query(FAQ).delete()
            self.db.commit()
        except Exception as exc:
            raise RepositoryError("Failed to delete faqs from the database") from exc
        