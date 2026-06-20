from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, UserDefinedType, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


class TimestampMixin:
    """Adds audit timestamps managed by PostgreSQL."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class UUIDPrimaryKeyMixin:
    """Adds a UUID primary key compatible with Supabase/PostgreSQL."""

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)


class Vector(UserDefinedType):
    """PostgreSQL pgvector column type for embeddings."""

    cache_ok = True

    def __init__(self, dimensions: int = 1536) -> None:
        self.dimensions = dimensions

    def get_col_spec(self, **_: object) -> str:
        return f"vector({self.dimensions})"
