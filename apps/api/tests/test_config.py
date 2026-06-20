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
