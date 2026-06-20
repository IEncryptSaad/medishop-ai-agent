from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class ContractModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


T = TypeVar("T")


class ErrorDetail(ContractModel):
    field: str | None = Field(default=None, description="Field or parameter that caused the error.")
    message: str = Field(description="Human-readable validation or domain error message.")


class ErrorResponse(ContractModel):
    success: bool = Field(default=False, description="Always false for error responses.")
    error: str = Field(description="Stable machine-readable error code.")
    message: str = Field(description="Human-readable error summary.")
    details: list[ErrorDetail] = Field(default_factory=list)
    request_id: str | None = Field(default=None, description="Correlation ID for support tracing.")


class SuccessEnvelope(ContractModel, Generic[T]):
    success: bool = Field(default=True, description="Always true for successful responses.")
    data: T
    message: str | None = Field(
        default=None, description="Optional human-readable success message."
    )
    request_id: str | None = Field(default=None, description="Correlation ID for support tracing.")


class PaginationParams(ContractModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PaginationMeta(ContractModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    has_next: bool
    has_previous: bool


class PaginatedResponse(ContractModel, Generic[T]):
    items: list[T]
    pagination: PaginationMeta


class TimestampedResource(ContractModel):
    created_at: datetime
    updated_at: datetime
