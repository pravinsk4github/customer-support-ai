import sqlite3
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.exception_handlers import (
    app_exception_handler,
    http_exception_handler, 
    unhandled_exception_handler, 
    validation_exception_handler
)
from app.api.middleware import RequestContextMiddleware
from app.core.exception import AppException
from app.database import engine
from app.models import Base
from app.api.routes_faq import router as faq_router
from app.api.routes_ingestion import router as ingestion_router
from app.api.routes_chat import router as chat_router
from app.schemas import HealthResponse, ReadinessResponse
from app.config import settings

app = FastAPI(title="Customer Support AI")

app.add_middleware(RequestContextMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)

Base.metadata.create_all(bind=engine)

app.include_router(faq_router)
app.include_router(ingestion_router)
app.include_router(chat_router)

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="OK")

@app.get("/ready", response_model=ReadinessResponse)
def ready_check():
    try:
        conn = sqlite3.connect(settings.database_url)
        conn.execute("SELECT 1")
        conn.close()
        return ReadinessResponse(status="OK")
    except sqlite3.Error:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready"}
        )


