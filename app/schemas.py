"""Request- und Response-Schemas mit Eingabevalidierung."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class LinkCreate(BaseModel):
    """Eingabe zum Anlegen eines Kurzlinks.

    `HttpUrl` lässt ausschliesslich http/https zu (Open-Redirect-Schutz).
    """

    target_url: HttpUrl
    alias: str | None = None


class LinkRead(BaseModel):
    """Ausgabe eines Kurzlinks inklusive vollständiger Kurz-URL."""

    code: str
    target_url: str
    short_url: str
    created_at: datetime


class StatsRead(BaseModel):
    """Klick-Statistik eines Kurzlinks: Gesamtzahl und Klicks pro Tag."""

    code: str
    total: int
    per_day: dict[str, int]


class UserCreate(BaseModel):
    """Eingabe für die Registrierung."""

    email: str
    password: str


class UserRead(BaseModel):
    """Öffentliche Benutzerdaten – ohne Passwort-Hash."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    created_at: datetime


class Token(BaseModel):
    """Bearer-Token als Login-Antwort."""

    access_token: str
    token_type: str = "bearer"
