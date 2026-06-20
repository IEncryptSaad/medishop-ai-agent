from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import Field

from app.contracts.common import (
    PaginatedResponse,
    PaginationParams,
    SuccessEnvelope,
    TimestampedResource,
)


class ProductListRequest(PaginationParams):
    category_id: UUID | None = None
    status: str | None = Field(default="active")
    min_price: Decimal | None = Field(default=None, ge=0)
    max_price: Decimal | None = Field(default=None, ge=0)


class ProductSearchRequest(PaginationParams):
    query: str = Field(min_length=1, max_length=240)
    category_id: UUID | None = None
    in_stock_only: bool = False
    min_price: Decimal | None = Field(default=None, ge=0)
    max_price: Decimal | None = Field(default=None, ge=0)
    attributes: dict[str, Any] = Field(default_factory=dict)


class ProductResponse(TimestampedResource):
    id: UUID
    category_id: UUID | None = None
    sku: str
    name: str
    description: str | None = None
    price: Decimal
    currency: str = Field(default="USD", min_length=3, max_length=3)
    stock_quantity: int = Field(ge=0)
    status: str
    shopify_product_id: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)


class ProductListResponse(PaginatedResponse[ProductResponse]):
    pass


ProductEnvelope = SuccessEnvelope[ProductResponse]
ProductListEnvelope = SuccessEnvelope[ProductListResponse]
ProductSearchEnvelope = SuccessEnvelope[ProductListResponse]
