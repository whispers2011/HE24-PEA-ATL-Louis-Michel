"""Anwendungs-Konfiguration aus Umgebungsvariablen bzw. .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Zentrale Einstellungen; Werte stammen aus .env oder der Umgebung."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./app.db"
    base_url: str = "http://localhost:8000"
    code_length: int = 6
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60


settings = Settings()
