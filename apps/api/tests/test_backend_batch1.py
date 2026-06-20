from app.main import create_app
from fastapi.testclient import TestClient

client = TestClient(create_app())


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"


def test_product_list() -> None:
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["pagination"]["total_items"] >= 1
    assert data["items"][0]["sku"]


def test_product_search() -> None:
    response = client.post(
        "/api/v1/products/search", json={"query": "sensitive moisturizer", "in_stock_only": True}
    )
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert any(item["sku"] == "CRM-001" for item in items)


def test_appointment_creation() -> None:
    response = client.post(
        "/api/v1/appointments",
        json={
            "appointment_type": "pharmacist_consultation",
            "scheduled_start": "2026-06-21T15:00:00Z",
            "scheduled_end": "2026-06-21T15:30:00Z",
            "notes": "Discuss skincare routine.",
        },
    )
    assert response.status_code == 201
    assert response.json()["data"]["status"] == "scheduled"


def test_support_ticket_creation() -> None:
    response = client.post(
        "/api/v1/support/tickets",
        json={
            "subject": "Order arrived damaged",
            "description": "The moisturizer bottle leaked during shipping.",
            "priority": "normal",
            "category": "order_issue",
        },
    )
    assert response.status_code == 201
    assert response.json()["data"]["status"] == "open"


def test_agent_chat_product_question() -> None:
    response = client.post(
        "/api/v1/agent/chat",
        json={
            "session_id": "test-products",
            "message": "Which moisturizer is good for sensitive skin?",
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["recommendations"]
    assert any(rec["type"] == "product" for rec in data["recommendations"])


def test_agent_chat_medical_faq_disclaimer() -> None:
    response = client.post(
        "/api/v1/agent/chat",
        json={
            "session_id": "test-medical",
            "message": "What should I do for cold symptoms and fever?",
        },
    )
    assert response.status_code == 200
    text = response.json()["data"]["response"].lower()
    assert "not a diagnosis" in text
    assert "healthcare professional" in text


def _create_appointment_for_validation() -> str:
    response = client.post(
        "/api/v1/appointments",
        json={
            "appointment_type": "pharmacist_consultation",
            "scheduled_start": "2026-06-22T15:00:00Z",
            "scheduled_end": "2026-06-22T15:30:00Z",
        },
    )
    assert response.status_code == 201
    return response.json()["data"]["id"]


def test_appointment_creation_mixed_timezone_awareness_returns_validation_error() -> None:
    response = client.post(
        "/api/v1/appointments",
        json={
            "appointment_type": "pharmacist_consultation",
            "scheduled_start": "2026-06-21T15:00:00+02:00",
            "scheduled_end": "2026-06-21T13:00:00",
        },
    )
    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"] == "validation_error"


def test_appointment_patch_scheduled_end_before_existing_start_is_rejected() -> None:
    appointment_id = _create_appointment_for_validation()

    response = client.patch(
        f"/api/v1/appointments/{appointment_id}",
        json={"scheduled_end": "2026-06-22T14:59:00Z"},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"] == "validation_error"


def test_appointment_patch_scheduled_start_after_existing_end_is_rejected() -> None:
    appointment_id = _create_appointment_for_validation()

    response = client.patch(
        f"/api/v1/appointments/{appointment_id}",
        json={"scheduled_start": "2026-06-22T15:31:00Z"},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"] == "validation_error"


def test_appointment_patch_explicit_null_for_required_fields_is_rejected() -> None:
    appointment_id = _create_appointment_for_validation()

    for field in ("scheduled_start", "scheduled_end", "status", "metadata"):
        response = client.patch(f"/api/v1/appointments/{appointment_id}", json={field: None})
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["error"] == "validation_error"
