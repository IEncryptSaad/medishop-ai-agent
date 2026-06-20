from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, Vector


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    full_name: Mapped[str | None] = mapped_column(String(200))
    phone: Mapped[str | None] = mapped_column(String(40))
    role: Mapped[str] = mapped_column(String(40), default="customer", nullable=False, index=True)
    external_customer_id: Mapped[str | None] = mapped_column(String(120), index=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)


class ProductCategory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "product_categories"

    name: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(180), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    parent_id: Mapped[UUID | None] = mapped_column(ForeignKey("product_categories.id"))
    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "products"

    category_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_categories.id"), index=True
    )
    sku: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(240), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False, index=True)
    shopify_product_id: Mapped[str | None] = mapped_column(String(120), unique=True)
    attributes: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    category: Mapped[ProductCategory | None] = relationship(back_populates="products")


class KnowledgeDocument(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "knowledge_documents"

    title: Mapped[str] = mapped_column(String(240), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    source_uri: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="draft", nullable=False, index=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    chunks: Mapped[list["KnowledgeChunk"]] = relationship(back_populates="document")


class KnowledgeChunk(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "knowledge_chunks"
    __table_args__ = (Index("ix_knowledge_chunks_document_position", "document_id", "chunk_index"),)

    document_id: Mapped[UUID] = mapped_column(ForeignKey("knowledge_documents.id"), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int | None] = mapped_column(Integer)
    embedding: Mapped[Any | None] = mapped_column(Vector(1536), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    document: Mapped[KnowledgeDocument] = relationship(back_populates="chunks")


class Appointment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "appointments"

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    appointment_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    scheduled_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    scheduled_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="scheduled", nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)


class SupportTicket(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "support_tickets"

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    subject: Mapped[str] = mapped_column(String(240), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="open", nullable=False, index=True)
    priority: Mapped[str] = mapped_column(String(40), default="normal", nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(100), index=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)


class Conversation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "conversations"

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    support_ticket_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("support_tickets.id"), index=True
    )
    channel: Mapped[str] = mapped_column(String(60), default="web", nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False, index=True)
    summary: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    messages: Mapped[list["Message"]] = relationship(back_populates="conversation")


class Message(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "messages"
    __table_args__ = (Index("ix_messages_conversation_created", "conversation_id", "created_at"),)

    conversation_id: Mapped[UUID] = mapped_column(ForeignKey("conversations.id"), nullable=False)
    sender_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    conversation: Mapped[Conversation] = relationship(back_populates="messages")


class AgentRun(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "agent_runs"

    conversation_id: Mapped[UUID | None] = mapped_column(ForeignKey("conversations.id"), index=True)
    support_ticket_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("support_tickets.id"), index=True
    )
    run_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", nullable=False, index=True)
    model_name: Mapped[str | None] = mapped_column(String(120))
    input_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    output_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
