from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base application exception for expected operational errors."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": {"message": exc.message}})
