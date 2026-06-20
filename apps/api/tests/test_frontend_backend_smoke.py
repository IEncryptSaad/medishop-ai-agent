from app.main import create_app
from fastapi.testclient import TestClient

client = TestClient(create_app())


def test_frontend_endpoint_batch_smoke_flow() -> None:
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["data"]["status"] == "ok"

    products = client.get("/api/v1/products")
    assert products.status_code == 200
    assert products.json()["data"]["items"]

    search = client.post("/api/v1/products/search", json={"query": "moisturizer"})
    assert search.status_code == 200
    assert search.json()["data"]["items"]

    appointment = client.post(
        "/api/v1/appointments",
        json={
            "appointment_type": "Pharmacist consultation",
            "scheduled_start": "2026-06-23T15:00:00Z",
            "scheduled_end": "2026-06-23T15:30:00Z",
            "notes": "Frontend smoke test booking.",
        },
    )
    assert appointment.status_code == 201
    appointment_id = appointment.json()["data"]["id"]

    appointments = client.get("/api/v1/appointments")
    assert appointments.status_code == 200
    assert any(item["id"] == appointment_id for item in appointments.json()["data"]["items"])

    patched_appointment = client.patch(
        f"/api/v1/appointments/{appointment_id}", json={"status": "confirmed"}
    )
    assert patched_appointment.status_code == 200
    assert patched_appointment.json()["data"]["status"] == "confirmed"

    ticket = client.post(
        "/api/v1/support/tickets",
        json={
            "subject": "Frontend smoke support ticket",
            "description": "Created by integration smoke test.",
            "priority": "normal",
            "category": "general",
        },
    )
    assert ticket.status_code == 201
    ticket_id = ticket.json()["data"]["id"]

    tickets = client.get("/api/v1/support/tickets")
    assert tickets.status_code == 200
    assert any(item["id"] == ticket_id for item in tickets.json()["data"]["items"])

    patched_ticket = client.patch(f"/api/v1/support/tickets/{ticket_id}", json={"status": "triage"})
    assert patched_ticket.status_code == 200
    assert patched_ticket.json()["data"]["status"] == "triage"

    chat = client.post(
        "/api/v1/agent/chat",
        json={"session_id": "frontend-smoke", "message": "Which moisturizer should I view?"},
    )
    assert chat.status_code == 200
    assert chat.json()["data"]["response"]
