from typing import Any
from uuid import UUID

from pydantic import Field

from app.contracts.common import ContractModel, SuccessEnvelope


class AgentChatRequest(ContractModel):
    session_id: str = Field(min_length=1, max_length=120)
    message: str = Field(min_length=1, max_length=4000)


class AgentSource(ContractModel):
    title: str
    source_type: str
    uri: str | None = None
    score: float | None = Field(default=None, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentRecommendation(ContractModel):
    id: UUID | str
    type: str = Field(description="Recommendation type, for example product or appointment.")
    title: str
    reason: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentChatResponse(ContractModel):
    response: str
    sources: list[AgentSource] = Field(default_factory=list)
    recommendations: list[AgentRecommendation] = Field(default_factory=list)
    conversation_id: str


AgentChatEnvelope = SuccessEnvelope[AgentChatResponse]
