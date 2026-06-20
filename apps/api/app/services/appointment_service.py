from __future__ import annotations

from math import ceil
from uuid import UUID

from fastapi import status

from app.contracts.appointments import (
    AppointmentCreateRequest,
    AppointmentListRequest,
    AppointmentListResponse,
    AppointmentUpdateRequest,
)
from app.contracts.common import PaginationMeta
from app.core.errors import AppError
from app.repositories.appointment_repository import appointment_repository


class AppointmentService:
    def __init__(self, repository=appointment_repository) -> None:
        self.repository = repository

    def create(self, payload: AppointmentCreateRequest):
        if payload.scheduled_end <= payload.scheduled_start:
            raise AppError(
                "scheduled_end must be after scheduled_start.",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                error="validation_error",
            )
        return self.repository.create(payload)

    def list(self, params: AppointmentListRequest) -> AppointmentListResponse:
        items = self.repository.list()
        if params.status:
            items = [i for i in items if i.status == params.status]
        if params.from_date:
            items = [i for i in items if i.scheduled_start >= params.from_date]
        if params.to_date:
            items = [i for i in items if i.scheduled_start <= params.to_date]
        total = len(items)
        start = (params.page - 1) * params.page_size
        return AppointmentListResponse(
            items=items[start : start + params.page_size],
            pagination=self._meta(params.page, params.page_size, total),
        )

    def get(self, appointment_id: UUID):
        item = self.repository.get(appointment_id)
        if item is None:
            raise AppError("Appointment not found.", status.HTTP_404_NOT_FOUND, error="not_found")
        return item

    def update(self, appointment_id: UUID, payload: AppointmentUpdateRequest):
        item = self.repository.update(appointment_id, payload)
        if item is None:
            raise AppError("Appointment not found.", status.HTTP_404_NOT_FOUND, error="not_found")
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
