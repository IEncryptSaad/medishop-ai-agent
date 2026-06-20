from __future__ import annotations

from math import ceil
from uuid import UUID

from fastapi import status

from app.contracts.common import PaginationMeta
from app.contracts.products import ProductListRequest, ProductListResponse, ProductSearchRequest
from app.core.errors import AppError
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository | None = None) -> None:
        self.repository = repository or ProductRepository()

    def list_products(self, params: ProductListRequest) -> ProductListResponse:
        items, total = self.repository.list(params)
        return ProductListResponse(
            items=items, pagination=self._meta(params.page, params.page_size, total)
        )

    def get_product(self, product_id: UUID):
        product = self.repository.get(product_id)
        if product is None:
            raise AppError("Product not found.", status.HTTP_404_NOT_FOUND, error="not_found")
        return product

    def search_products(self, params: ProductSearchRequest) -> ProductListResponse:
        items, total = self.repository.search(params)
        return ProductListResponse(
            items=items, pagination=self._meta(params.page, params.page_size, total)
        )

    @staticmethod
    def _meta(page: int, page_size: int, total: int) -> PaginationMeta:
        pages = ceil(total / page_size) if total else 0
        return PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=pages,
            has_next=page < pages,
            has_previous=page > 1,
        )
