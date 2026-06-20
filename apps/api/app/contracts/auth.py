from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field

from app.contracts.common import ContractModel, SuccessEnvelope, TimestampedResource


class RegisterRequest(ContractModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=200)
    phone: str | None = Field(default=None, max_length=40)


class LoginRequest(ContractModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RefreshTokenRequest(ContractModel):
    refresh_token: str = Field(min_length=1)


class UserResponse(TimestampedResource):
    id: UUID
    email: EmailStr
    full_name: str | None = None
    phone: str | None = None
    role: str = "customer"


class TokenResponse(ContractModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserResponse


CurrentUserEnvelope = SuccessEnvelope[UserResponse]
AuthEnvelope = SuccessEnvelope[TokenResponse]
