from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from app.contracts.products import ProductListRequest, ProductResponse, ProductSearchRequest

NOW = datetime(2026, 6, 20, 12, 0, tzinfo=UTC)

DEMO_PRODUCTS: list[ProductResponse] = [
    ProductResponse(
        id=UUID("22222222-2222-2222-2222-222222222222"),
        sku="CRM-001",
        name="Ceramide Daily Moisturizer",
        description="Fragrance-free moisturizer for dry or sensitive skin with ceramides.",
        price=Decimal("24.99"),
        stock_quantity=12,
        status="active",
        shopify_product_id="gid://shopify/Product/1",
        attributes={"skin_type": "sensitive", "fragrance_free": True, "category": "skincare"},
        created_at=NOW,
        updated_at=NOW,
    ),
    ProductResponse(
        id=UUID("22222222-2222-2222-2222-222222222223"),
        sku="SUN-050",
        name="Mineral SPF 50 Sunscreen",
        description="Broad-spectrum mineral sunscreen for face and body.",
        price=Decimal("18.50"),
        stock_quantity=20,
        status="active",
        attributes={"skin_type": "all", "spf": 50, "category": "sun_care"},
        created_at=NOW,
        updated_at=NOW,
    ),
    ProductResponse(
        id=UUID("22222222-2222-2222-2222-222222222224"),
        sku="COLD-010",
        name="Saline Nasal Spray",
        description="Drug-free saline spray for nasal dryness and congestion support.",
        price=Decimal("7.99"),
        stock_quantity=0,
        status="active",
        attributes={"category": "cold_flu", "drug_free": True},
        created_at=NOW,
        updated_at=NOW,
    ),
]


class ProductRepository:
    def list(self, params: ProductListRequest) -> tuple[list[ProductResponse], int]:
        products = [p for p in DEMO_PRODUCTS if params.status is None or p.status == params.status]
        if params.category_id:
            products = [p for p in products if p.category_id == params.category_id]
        products = self._filter_price(products, params.min_price, params.max_price)
        return self._paginate(products, params.page, params.page_size)

    def get(self, product_id: UUID) -> ProductResponse | None:
        return next((p for p in DEMO_PRODUCTS if p.id == product_id), None)

    def search(self, params: ProductSearchRequest) -> tuple[list[ProductResponse], int]:
        terms = [term.strip().lower() for term in params.query.split() if term.strip()]
        products = []
        for product in DEMO_PRODUCTS:
            haystack = " ".join(
                [
                    product.name,
                    product.description or "",
                    *(str(value) for value in product.attributes.values()),
                ]
            ).lower()
            if any(term in haystack for term in terms):
                products.append(product)
        if params.in_stock_only:
            products = [p for p in products if p.stock_quantity > 0]
        if params.category_id:
            products = [p for p in products if p.category_id == params.category_id]
        for key, value in params.attributes.items():
            products = [p for p in products if p.attributes.get(key) == value]
        products = self._filter_price(products, params.min_price, params.max_price)
        return self._paginate(products, params.page, params.page_size)

    @staticmethod
    def _filter_price(products, min_price, max_price):
        if min_price is not None:
            products = [p for p in products if p.price >= min_price]
        if max_price is not None:
            products = [p for p in products if p.price <= max_price]
        return products

    @staticmethod
    def _paginate(
        items: list[ProductResponse], page: int, page_size: int
    ) -> tuple[list[ProductResponse], int]:
        start = (page - 1) * page_size
        return items[start : start + page_size], len(items)
