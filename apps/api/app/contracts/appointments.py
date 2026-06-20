from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import Field

from app.contracts.common import (
    ContractModel,
    PaginatedResponse,
    PaginationParams,
    SuccessEnvelope,
    TimestampedResource,
)


class AppointmentCreateRequest(ContractModel):
    appointment_type: str = Field(min_length=1, max_length=120)
    scheduled_start: datetime
    scheduled_end: datetime
    notes: str | None = Field(default=None, max_length=2000)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AppointmentListRequest(PaginationParams):
    status: str | None = None
    from_date: datetime | None = None
    to_date: datetime | None = None


class AppointmentUpdateRequest(ContractModel):
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None
    status: str | None = Field(default=None, max_length=40)
    notes: str | None = Field(default=None, max_length=2000)
    metadata: dict[str, Any] | None = None


class AppointmentResponse(TimestampedResource):
    id: UUID
    user_id: UUID | None = None
    appointment_type: str
    scheduled_start: datetime
    scheduled_end: datetime
    status: str
    notes: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AppointmentListResponse(PaginatedResponse[AppointmentResponse]):
    pass


AppointmentEnvelope = SuccessEnvelope[AppointmentResponse]
AppointmentListEnvelope = SuccessEnvelope[AppointmentListResponse]
