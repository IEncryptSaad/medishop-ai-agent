from functools import lru_cache
from pathlib import Path

from pydantic import Field
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

    # Keep this as a plain string so Pydantic Settings never tries to JSON-parse
    # Render-provided values before our application can normalize them.
    api_cors_origins_raw: str = Field(
        default="http://localhost:3000", validation_alias="API_CORS_ORIGINS"
    )

    @property
    def api_cors_origins(self) -> list[str]:
        raw_value = self.api_cors_origins_raw.strip()
        if not raw_value:
            return ["http://localhost:3000"]

        return [
            origin.strip().rstrip("/")
            for origin in raw_value.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
