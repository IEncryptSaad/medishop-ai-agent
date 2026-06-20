from pathlib import Path

from app.core.config import ROOT_ENV_FILE, Settings


def test_env_file_points_to_repo_root(monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[3]

    monkeypatch.chdir(repo_root / "apps" / "api")

    assert ROOT_ENV_FILE == repo_root / ".env"
    assert Settings.model_config["env_file"] == ROOT_ENV_FILE


def test_environment_variables_override_env_file(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")

    settings = Settings()

    assert settings.app_env == "production"


def test_default_cors_origin_matches_browser_origin(monkeypatch) -> None:
    monkeypatch.delenv("API_CORS_ORIGINS", raising=False)

    settings = Settings(_env_file=None)

    assert settings.api_cors_origins == ["http://localhost:3000"]


def test_cors_origins_are_split_validated_and_normalized(monkeypatch) -> None:
    monkeypatch.setenv(
        "API_CORS_ORIGINS",
        "http://localhost:3000/, https://example.com/, http://127.0.0.1:5173",
    )

    settings = Settings(_env_file=None)

    assert settings.api_cors_origins == [
        "http://localhost:3000",
        "https://example.com",
        "http://127.0.0.1:5173",
    ]
