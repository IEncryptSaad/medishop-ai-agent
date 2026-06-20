from datetime import UTC, datetime

from fastapi import APIRouter, Request

from app.contracts.common import SuccessEnvelope
from app.contracts.health import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=SuccessEnvelope[HealthResponse])
def health_check(request: Request) -> SuccessEnvelope[HealthResponse]:
    return SuccessEnvelope(
        data=HealthResponse(status="ok", version="0.1.0", timestamp=datetime.now(UTC)),
        request_id=request.headers.get("x-request-id"),
    )
