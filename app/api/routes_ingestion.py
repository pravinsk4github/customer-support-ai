from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

@router.post("/sync")
def sync_faqs(db: Session = Depends(get_db)):
    service = IngestionService(db)
    count = service.sync_faqs_to_vector_store()
    return {
        "status": "success",
        "synced_faqs": count
    }
