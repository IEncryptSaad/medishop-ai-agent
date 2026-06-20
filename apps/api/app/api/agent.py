from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.contracts.agent import AgentChatRequest, AgentChatResponse
from app.contracts.common import SuccessEnvelope
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agent", tags=["agent"])


def get_agent_service() -> AgentService:
    return AgentService()


@router.post("/chat", response_model=SuccessEnvelope[AgentChatResponse])
def chat(
    payload: AgentChatRequest,
    request: Request,
    service: Annotated[AgentService, Depends(get_agent_service)],
):
    return SuccessEnvelope(
        data=service.chat(payload), request_id=request.headers.get("x-request-id")
    )
