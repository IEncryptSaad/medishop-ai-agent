from datetime import datetime

from app.contracts.common import ContractModel, SuccessEnvelope


class HealthResponse(ContractModel):
    status: str = "ok"
    version: str
    timestamp: datetime


HealthEnvelope = SuccessEnvelope[HealthResponse]
