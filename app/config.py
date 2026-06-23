"""Anwendungs-Konfiguration aus Umgebungsvariablen bzw. .env."""

from pydantic import Field
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
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    # Pflichtwert ohne In-Code-Default: das JWT-Signatur-Secret gehört
    # ausschliesslich in die .env. Ohne gesetztes SECRET_KEY startet die App nicht.
    secret_key: str
    access_token_expire_minutes: int = 60


settings = Settings()  # type: ignore[call-arg]  # secret_key stammt aus .env/Umgebung
