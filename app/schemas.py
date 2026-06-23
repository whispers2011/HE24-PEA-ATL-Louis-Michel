"""Request- und Response-Schemas mit Eingabevalidierung."""

from pydantic import BaseModel, HttpUrl


class LinkCreate(BaseModel):
    """Eingabe zum Anlegen eines Kurzlinks.

    `HttpUrl` lässt ausschliesslich http/https zu (Open-Redirect-Schutz).
    """

    target_url: HttpUrl
    alias: str | None = None
