from __future__ import annotations

from math import ceil
from uuid import UUID

from fastapi import status

from app.contracts.common import PaginationMeta
from app.contracts.support import (
    SupportTicketCreateRequest,
    SupportTicketListRequest,
    SupportTicketListResponse,
    SupportTicketUpdateRequest,
)
from app.core.errors import AppError
from app.repositories.support_repository import support_repository


class SupportService:
    def __init__(self, repository=support_repository) -> None:
        self.repository = repository

    def create(self, payload: SupportTicketCreateRequest):
        return self.repository.create(payload)

    def list(self, params: SupportTicketListRequest) -> SupportTicketListResponse:
        items = self.repository.list()
        if params.status:
            items = [i for i in items if i.status == params.status]
        if params.priority:
            items = [i for i in items if i.priority == params.priority]
        if params.category:
            items = [i for i in items if i.category == params.category]
        if params.created_from:
            items = [i for i in items if i.created_at >= params.created_from]
        if params.created_to:
            items = [i for i in items if i.created_at <= params.created_to]
        total = len(items)
        start = (params.page - 1) * params.page_size
        return SupportTicketListResponse(
            items=items[start : start + params.page_size],
            pagination=self._meta(params.page, params.page_size, total),
        )

    def get(self, ticket_id: UUID):
        item = self.repository.get(ticket_id)
        if item is None:
            raise AppError(
                "Support ticket not found.", status.HTTP_404_NOT_FOUND, error="not_found"
            )
        return item

    def update(self, ticket_id: UUID, payload: SupportTicketUpdateRequest):
        item = self.repository.update(ticket_id, payload)
        if item is None:
            raise AppError(
                "Support ticket not found.", status.HTTP_404_NOT_FOUND, error="not_found"
            )
        return item

    @staticmethod
    def _meta(page, page_size, total):
        pages = ceil(total / page_size) if total else 0
        return PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=pages,
            has_next=page < pages,
            has_previous=page > 1,
        )
