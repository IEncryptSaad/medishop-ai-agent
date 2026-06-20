from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

from app.contracts.appointments import AppointmentResponse
from app.contracts.support import SupportTicketResponse


def _timestamp() -> datetime:
    return datetime(2026, 6, 20, 12, 0, tzinfo=UTC)


def test_appointment_response_reads_orm_metadata_json_and_serializes_metadata() -> None:
    appointment = SimpleNamespace(
        id=uuid4(),
        user_id=uuid4(),
        appointment_type="consultation",
        scheduled_start=_timestamp(),
        scheduled_end=_timestamp(),
        status="scheduled",
        notes="Bring prescription",
        metadata_json={"source": "review-test"},
        metadata={"should": "not-be-used"},
        created_at=_timestamp(),
        updated_at=_timestamp(),
    )

    response = AppointmentResponse.model_validate(appointment)

    assert response.metadata == {"source": "review-test"}
    assert response.model_dump(by_alias=True)["metadata"] == {"source": "review-test"}
    assert "metadata_json" not in response.model_dump(by_alias=True)


def test_support_ticket_response_reads_orm_metadata_json_and_serializes_metadata() -> None:
    ticket = SimpleNamespace(
        id=uuid4(),
        user_id=uuid4(),
        subject="Order question",
        description="Where is my order?",
        status="open",
        priority="normal",
        category="orders",
        metadata_json={"channel": "web"},
        metadata={"should": "not-be-used"},
        created_at=_timestamp(),
        updated_at=_timestamp(),
    )

    response = SupportTicketResponse.model_validate(ticket)

    assert response.metadata == {"channel": "web"}
    assert response.model_dump(by_alias=True)["metadata"] == {"channel": "web"}
    assert "metadata_json" not in response.model_dump(by_alias=True)
