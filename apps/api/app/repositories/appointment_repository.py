from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.contracts.appointments import (
    AppointmentCreateRequest,
    AppointmentResponse,
    AppointmentUpdateRequest,
)


class AppointmentRepository:
    def __init__(self) -> None:
        self._appointments: dict[UUID, AppointmentResponse] = {}

    def create(self, payload: AppointmentCreateRequest) -> AppointmentResponse:
        now = datetime.now(UTC)
        item = AppointmentResponse(
            id=uuid4(),
            user_id=None,
            appointment_type=payload.appointment_type,
            scheduled_start=payload.scheduled_start,
            scheduled_end=payload.scheduled_end,
            status="scheduled",
            notes=payload.notes,
            metadata_json=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        self._appointments[item.id] = item
        return item

    def list(self) -> list[AppointmentResponse]:
        return sorted(self._appointments.values(), key=lambda a: a.scheduled_start)

    def get(self, appointment_id: UUID) -> AppointmentResponse | None:
        return self._appointments.get(appointment_id)

    def update(
        self, appointment_id: UUID, payload: AppointmentUpdateRequest
    ) -> AppointmentResponse | None:
        current = self.get(appointment_id)
        if current is None:
            return None
        data = current.model_dump()
        updates = payload.model_dump(exclude_unset=True)
        if "metadata" in updates:
            updates["metadata_json"] = updates.pop("metadata")
        data.update(updates)
        data["updated_at"] = datetime.now(UTC)
        updated = AppointmentResponse.model_validate(data)
        self._appointments[appointment_id] = updated
        return updated


appointment_repository = AppointmentRepository()
