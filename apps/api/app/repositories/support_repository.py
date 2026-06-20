from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.contracts.support import (
    SupportTicketCreateRequest,
    SupportTicketResponse,
    SupportTicketUpdateRequest,
)


class SupportRepository:
    def __init__(self) -> None:
        self._tickets: dict[UUID, SupportTicketResponse] = {}

    def create(self, payload: SupportTicketCreateRequest) -> SupportTicketResponse:
        now = datetime.now(UTC)
        ticket = SupportTicketResponse(
            id=uuid4(),
            user_id=None,
            subject=payload.subject,
            description=payload.description,
            status="open",
            priority=payload.priority,
            category=payload.category,
            metadata_json=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        self._tickets[ticket.id] = ticket
        return ticket

    def list(self) -> list[SupportTicketResponse]:
        return sorted(self._tickets.values(), key=lambda t: t.created_at, reverse=True)

    def get(self, ticket_id: UUID) -> SupportTicketResponse | None:
        return self._tickets.get(ticket_id)

    def update(
        self, ticket_id: UUID, payload: SupportTicketUpdateRequest
    ) -> SupportTicketResponse | None:
        current = self.get(ticket_id)
        if current is None:
            return None
        data = current.model_dump()
        updates = payload.model_dump(exclude_unset=True)
        if "metadata" in updates:
            updates["metadata_json"] = updates.pop("metadata")
        data.update(updates)
        data["updated_at"] = datetime.now(UTC)
        updated = SupportTicketResponse.model_validate(data)
        self._tickets[ticket_id] = updated
        return updated


support_repository = SupportRepository()
