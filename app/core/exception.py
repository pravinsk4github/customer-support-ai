from fastapi import status

class ErrorCodes:
    RESOURCE_NOT_FOUND = "resource_not_found"
    INVALID_REQUEST = "invalid_request"
    DATABASE_ERROR = "database_error"
    INTERNAL_SERVER_ERROR = "internal_server_error"

class AppException(Exception):
    """Base exception for know application error"""

    def __init__(self, message: str, code: str, status_code: int) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(
            message=message, 
            code=ErrorCodes.RESOURCE_NOT_FOUND, 
            status_code=status.HTTP_404_NOT_FOUND,
        )

class BadRequestError(AppException):
    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(
            message=message,
            code=ErrorCodes.INVALID_REQUEST,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

class ConflictError(AppException):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(
            message=message,
            code="conflict",
            status_code=status.HTTP_409_CONFLICT,
        )

class RepositoryError(AppException):
    def __init__(self, message: str = "Data access error") -> None:
        super().__init__(
            message=message,
            code=ErrorCodes.DATABASE_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
