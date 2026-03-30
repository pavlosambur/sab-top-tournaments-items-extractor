"""Project settings loaded from .env files via pydantic-settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ENV = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    """Main project settings from .env."""

    model_config = SettingsConfigDict(env_file=PROJECT_ENV)

    google_service_account_path: str
    backoffice_env_file: str


class BackofficeCredentials(BaseSettings):
    """Backoffice credentials from external .env file."""

    model_config = SettingsConfigDict(env_file=Settings().backoffice_env_file)  # type: ignore[call-arg]

    backoffice_login: str
    backoffice_password: str


settings = Settings()  # type: ignore[call-arg]
credentials = BackofficeCredentials()  # type: ignore[call-arg]
