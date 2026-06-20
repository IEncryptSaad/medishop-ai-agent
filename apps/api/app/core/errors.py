from __future__ import annotations

import logging
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base application exception for expected operational errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error: str = "bad_request",
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error = error
        self.details = details or []
        super().__init__(message)


def _request_id(request: Request) -> str | None:
    return request.headers.get("x-request-id")


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.warning(
        "request_failed",
        extra={"path": request.url.path, "error": exc.error, "status_code": exc.status_code},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.error,
            "message": exc.message,
            "details": exc.details,
            "request_id": _request_id(request),
        },
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("validation_failed", extra={"path": request.url.path, "errors": exc.errors()})
    details = [
        {
            "field": ".".join(str(part) for part in err.get("loc", [])),
            "message": err.get("msg", "Invalid value."),
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "validation_error",
            "message": "One or more request fields are invalid.",
            "details": details,
            "request_id": _request_id(request),
        },
    )


async def http_error_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = "not_found" if exc.status_code == status.HTTP_404_NOT_FOUND else "http_error"
    logger.warning("http_failed", extra={"path": request.url.path, "status_code": exc.status_code})
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": code,
            "message": str(exc.detail),
            "details": [],
            "request_id": _request_id(request),
        },
    )
