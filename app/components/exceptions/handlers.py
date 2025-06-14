from fastapi import Request
from fastapi.responses import JSONResponse

from app.components.exceptions import ApplicationException


def application_exception_handler(request: Request, exc: ApplicationException) -> JSONResponse:
    """
    Обработчик исключений приложения
    """
    return JSONResponse(
        content={
            "error": exc.name,
            "message": exc.message
        },
        status_code=exc.code
    )