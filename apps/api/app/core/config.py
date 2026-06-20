from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[4]
ROOT_ENV_FILE = REPO_ROOT / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=ROOT_ENV_FILE, env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "MediShop AI Agent API"
    app_env: str = Field(default="development", validation_alias="APP_ENV")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    api_host: str = Field(default="0.0.0.0", validation_alias="API_HOST")
    api_port: int = Field(default=8000, validation_alias="API_PORT")
    llm_provider: str = Field(default="mock", validation_alias="LLM_PROVIDER")
    api_cors_origins: list[AnyHttpUrl] = Field(
        default_factory=list, validation_alias="API_CORS_ORIGINS"
    )

    @field_validator("api_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
