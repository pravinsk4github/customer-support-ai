import uuid
from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exception import AppException
from app.api.error_responses import ErrorResponse, ErrorDetail
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        "HTTP exception raised",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code,
            "detail": exc.detail,
        },
    )

    response = ErrorResponse(
        error=ErrorDetail(
            code="http_error",
            message=str(exc.detail)
        ),
        request_id=request_id
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )

async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:     
    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        f"Request validation failed | path={request.url.path} | method={request.method} | errors={exc.errors()}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "errors": exc.errors(),
        },
    )

    response = ErrorResponse(
        error=ErrorDetail(
            code="validation_error",
            message="Invalid request payload",
        ),
        request_id=request_id,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=response.model_dump(),
    )

async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")

    logger.exception(
        "Unhandled exception occurred",
        extra={
            "path": request.url.path,
            "method": request.method,
            "exception_type": type(exc).__name__,
        },
    )

    response = ErrorResponse(
        error=ErrorDetail(
            code="internal_server_error",
            message="Something went wrong. Please try again later.",
        ),
        request_id=request_id,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(),
    )

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        "Application exception raised",
        extra={
            "path": request.url.path,
            "method": request.method,
            "error_code": exc.code,
            "status_code": exc.status_code,
            "exc_message": exc.message,
        },
    )

    response = ErrorResponse(
        error=ErrorDetail(
            code=exc.code,
            message=exc.message,
        ),
        request_id=request_id,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
    )