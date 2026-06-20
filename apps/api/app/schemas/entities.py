from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Timestamped(ORMBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserBase(ORMBase):
    email: str
    full_name: str | None = None
    phone: str | None = None
    role: str = "customer"
    external_customer_id: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class UserCreate(UserBase):
    pass


class UserRead(UserBase, Timestamped):
    pass


class ProductCategoryBase(ORMBase):
    name: str
    slug: str
    description: str | None = None
    parent_id: UUID | None = None


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryRead(ProductCategoryBase, Timestamped):
    pass


class ProductBase(ORMBase):
    category_id: UUID | None = None
    sku: str
    name: str
    description: str | None = None
    price: Decimal
    currency: str = "USD"
    stock_quantity: int = 0
    status: str = "active"
    shopify_product_id: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase, Timestamped):
    pass


class KnowledgeDocumentBase(ORMBase):
    title: str
    source_type: str
    source_uri: str | None = None
    status: str = "draft"
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class KnowledgeDocumentCreate(KnowledgeDocumentBase):
    pass


class KnowledgeDocumentRead(KnowledgeDocumentBase, Timestamped):
    pass


class KnowledgeChunkBase(ORMBase):
    document_id: UUID
    chunk_index: int
    content: str
    token_count: int | None = None
    embedding: list[float] | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class KnowledgeChunkCreate(KnowledgeChunkBase):
    pass


class KnowledgeChunkRead(KnowledgeChunkBase, Timestamped):
    pass


class AppointmentBase(ORMBase):
    user_id: UUID | None = None
    appointment_type: str
    scheduled_start: datetime
    scheduled_end: datetime
    status: str = "scheduled"
    notes: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase, Timestamped):
    pass


class SupportTicketBase(ORMBase):
    user_id: UUID | None = None
    subject: str
    description: str
    status: str = "open"
    priority: str = "normal"
    category: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class SupportTicketCreate(SupportTicketBase):
    pass


class SupportTicketRead(SupportTicketBase, Timestamped):
    pass


class ConversationBase(ORMBase):
    user_id: UUID | None = None
    support_ticket_id: UUID | None = None
    channel: str = "web"
    status: str = "active"
    summary: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase, Timestamped):
    pass


class MessageBase(ORMBase):
    conversation_id: UUID
    sender_type: str
    content: str
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase, Timestamped):
    pass


class AgentRunBase(ORMBase):
    conversation_id: UUID | None = None
    support_ticket_id: UUID | None = None
    run_type: str
    status: str = "queued"
    model_name: str | None = None
    input_payload: dict[str, Any] = Field(default_factory=dict)
    output_payload: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class AgentRunCreate(AgentRunBase):
    pass


class AgentRunRead(AgentRunBase, Timestamped):
    pass
