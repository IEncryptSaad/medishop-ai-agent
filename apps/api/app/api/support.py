from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from app.contracts.common import SuccessEnvelope
from app.contracts.support import (
    SupportTicketCreateRequest,
    SupportTicketListRequest,
    SupportTicketListResponse,
    SupportTicketResponse,
    SupportTicketUpdateRequest,
)
from app.services.support_service import SupportService

router = APIRouter(prefix="/support/tickets", tags=["support"])


def get_support_service() -> SupportService:
    return SupportService()


@router.post("", response_model=SuccessEnvelope[SupportTicketResponse], status_code=201)
def create_ticket(
    payload: SupportTicketCreateRequest,
    request: Request,
    service: Annotated[SupportService, Depends(get_support_service)],
):
    return SuccessEnvelope(
        data=service.create(payload),
        message="Support ticket created.",
        request_id=request.headers.get("x-request-id"),
    )


@router.get("", response_model=SuccessEnvelope[SupportTicketListResponse])
def list_tickets(
    request: Request,
    params: Annotated[SupportTicketListRequest, Depends()],
    service: Annotated[SupportService, Depends(get_support_service)],
):
    return SuccessEnvelope(
        data=service.list(params), request_id=request.headers.get("x-request-id")
    )


@router.get("/{ticket_id}", response_model=SuccessEnvelope[SupportTicketResponse])
def get_ticket(
    ticket_id: UUID,
    request: Request,
    service: Annotated[SupportService, Depends(get_support_service)],
):
    return SuccessEnvelope(
        data=service.get(ticket_id), request_id=request.headers.get("x-request-id")
    )


@router.patch("/{ticket_id}", response_model=SuccessEnvelope[SupportTicketResponse])
def update_ticket(
    ticket_id: UUID,
    payload: SupportTicketUpdateRequest,
    request: Request,
    service: Annotated[SupportService, Depends(get_support_service)],
):
    return SuccessEnvelope(
        data=service.update(ticket_id, payload), request_id=request.headers.get("x-request-id")
    )
