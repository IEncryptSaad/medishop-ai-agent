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


class SupportTicketCreateRequest(ContractModel):
    subject: str = Field(min_length=1, max_length=240)
    description: str = Field(min_length=1, max_length=5000)
    priority: str = Field(default="normal", max_length=40)
    category: str | None = Field(default=None, max_length=100)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SupportTicketListRequest(PaginationParams):
    status: str | None = None
    priority: str | None = None
    category: str | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None


class SupportTicketUpdateRequest(ContractModel):
    subject: str | None = Field(default=None, min_length=1, max_length=240)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    status: str | None = Field(default=None, max_length=40)
    priority: str | None = Field(default=None, max_length=40)
    category: str | None = Field(default=None, max_length=100)
    metadata: dict[str, Any] | None = None


class SupportTicketResponse(TimestampedResource):
    id: UUID
    user_id: UUID | None = None
    subject: str
    description: str
    status: str
    priority: str
    category: str | None = None
    metadata: dict[str, Any] = Field(
        default_factory=dict, validation_alias="metadata_json", serialization_alias="metadata"
    )


class SupportTicketListResponse(PaginatedResponse[SupportTicketResponse]):
    pass


SupportTicketEnvelope = SuccessEnvelope[SupportTicketResponse]
SupportTicketListEnvelope = SuccessEnvelope[SupportTicketListResponse]
