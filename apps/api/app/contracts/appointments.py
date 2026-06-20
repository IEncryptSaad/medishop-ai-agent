from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.contracts.common import (
    ContractModel,
    PaginatedResponse,
    PaginationParams,
    SuccessEnvelope,
    TimestampedResource,
)


def _normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


class AppointmentCreateRequest(ContractModel):
    appointment_type: str = Field(min_length=1, max_length=120)
    scheduled_start: datetime
    scheduled_end: datetime
    notes: str | None = Field(default=None, max_length=2000)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("scheduled_start", "scheduled_end")
    @classmethod
    def normalize_scheduled_datetime(cls, value: datetime) -> datetime:
        return _normalize_datetime(value)

    @model_validator(mode="after")
    def validate_scheduled_duration(self) -> "AppointmentCreateRequest":
        if self.scheduled_end <= self.scheduled_start:
            raise ValueError("scheduled_end must be after scheduled_start.")
        return self


class AppointmentListRequest(PaginationParams):
    status: str | None = None
    from_date: datetime | None = None
    to_date: datetime | None = None

    @field_validator("from_date", "to_date")
    @classmethod
    def normalize_filter_datetime(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return _normalize_datetime(value)


class AppointmentUpdateRequest(ContractModel):
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None
    status: str | None = Field(default=None, max_length=40)
    notes: str | None = Field(default=None, max_length=2000)
    metadata: dict[str, Any] | None = None

    @model_validator(mode="before")
    @classmethod
    def reject_required_field_nulls(cls, data: Any) -> Any:
        if isinstance(data, dict):
            required_fields = {"scheduled_start", "scheduled_end", "status", "metadata"}
            null_fields = sorted(field for field in required_fields if data.get(field, ...) is None)
            if null_fields:
                fields = ", ".join(null_fields)
                raise ValueError(f"Required appointment fields cannot be null: {fields}.")
        return data

    @field_validator("scheduled_start", "scheduled_end")
    @classmethod
    def normalize_scheduled_datetime(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return _normalize_datetime(value)


class AppointmentResponse(TimestampedResource):
    id: UUID
    user_id: UUID | None = None
    appointment_type: str
    scheduled_start: datetime
    scheduled_end: datetime
    status: str
    notes: str | None = None
    metadata: dict[str, Any] = Field(
        default_factory=dict, validation_alias="metadata_json", serialization_alias="metadata"
    )


class AppointmentListResponse(PaginatedResponse[AppointmentResponse]):
    pass


AppointmentEnvelope = SuccessEnvelope[AppointmentResponse]
AppointmentListEnvelope = SuccessEnvelope[AppointmentListResponse]
