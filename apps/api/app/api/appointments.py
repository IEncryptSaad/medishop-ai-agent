from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from app.contracts.appointments import (
    AppointmentCreateRequest,
    AppointmentListRequest,
    AppointmentListResponse,
    AppointmentResponse,
    AppointmentUpdateRequest,
)
from app.contracts.common import SuccessEnvelope
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"])


def get_appointment_service() -> AppointmentService:
    return AppointmentService()


@router.post("", response_model=SuccessEnvelope[AppointmentResponse], status_code=201)
def create_appointment(
    payload: AppointmentCreateRequest,
    request: Request,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
):
    return SuccessEnvelope(
        data=service.create(payload),
        message="Appointment created.",
        request_id=request.headers.get("x-request-id"),
    )


@router.get("", response_model=SuccessEnvelope[AppointmentListResponse])
def list_appointments(
    request: Request,
    params: Annotated[AppointmentListRequest, Depends()],
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
):
    return SuccessEnvelope(
        data=service.list(params), request_id=request.headers.get("x-request-id")
    )


@router.get("/{appointment_id}", response_model=SuccessEnvelope[AppointmentResponse])
def get_appointment(
    appointment_id: UUID,
    request: Request,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
):
    return SuccessEnvelope(
        data=service.get(appointment_id), request_id=request.headers.get("x-request-id")
    )


@router.patch("/{appointment_id}", response_model=SuccessEnvelope[AppointmentResponse])
def update_appointment(
    appointment_id: UUID,
    payload: AppointmentUpdateRequest,
    request: Request,
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
):
    return SuccessEnvelope(
        data=service.update(appointment_id, payload), request_id=request.headers.get("x-request-id")
    )
