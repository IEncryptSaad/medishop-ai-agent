from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from app.contracts.common import SuccessEnvelope
from app.contracts.products import (
    ProductListRequest,
    ProductListResponse,
    ProductResponse,
    ProductSearchRequest,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service() -> ProductService:
    return ProductService()


@router.get("", response_model=SuccessEnvelope[ProductListResponse])
def list_products(
    request: Request,
    params: Annotated[ProductListRequest, Depends()],
    service: Annotated[ProductService, Depends(get_product_service)],
):
    return SuccessEnvelope(
        data=service.list_products(params), request_id=request.headers.get("x-request-id")
    )


@router.post("/search", response_model=SuccessEnvelope[ProductListResponse])
def search_products(
    payload: ProductSearchRequest,
    request: Request,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    return SuccessEnvelope(
        data=service.search_products(payload), request_id=request.headers.get("x-request-id")
    )


@router.get("/{product_id}", response_model=SuccessEnvelope[ProductResponse])
def get_product(
    product_id: UUID,
    request: Request,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    return SuccessEnvelope(
        data=service.get_product(product_id), request_id=request.headers.get("x-request-id")
    )
