from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base exception for the application."""
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code


class NotFoundException(AppException):
    """Resource not found."""
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(detail=detail, status_code=404)


class ConflictException(AppException):
    """Resource already exists."""
    def __init__(self, detail: str = "El recurso ya existe"):
        super().__init__(detail=detail, status_code=409)


class UnauthorizedException(AppException):
    """Authentication required."""
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(detail=detail, status_code=401)


class ForbiddenException(AppException):
    """Access denied."""
    def __init__(self, detail: str = "Acceso denegado"):
        super().__init__(detail=detail, status_code=403)


class ValidationException(AppException):
    """Business rule validation failed."""
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=400)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
