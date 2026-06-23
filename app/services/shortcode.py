"""Erzeugung eindeutiger Kurzcodes und Validierung von Wunsch-Aliassen."""

import re
import secrets

from sqlmodel import Session, select

from app.config import settings
from app.models import Link

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
ALIAS_PATTERN = re.compile(r"[A-Za-z0-9_-]{3,32}")


def generate_code(length: int | None = None) -> str:
    """Erzeugt einen zufälligen Kurzcode aus dem erlaubten Zeichensatz."""
    size = settings.code_length if length is None else length
    return "".join(secrets.choice(ALPHABET) for _ in range(size))


def is_valid_alias(alias: str) -> bool:
    """Prüft einen Wunsch-Alias: 3–32 Zeichen aus `[A-Za-z0-9_-]`."""
    return ALIAS_PATTERN.fullmatch(alias) is not None


def code_exists(session: Session, code: str) -> bool:
    """Gibt an, ob bereits ein Link mit diesem Code existiert."""
    return session.exec(select(Link).where(Link.code == code)).first() is not None


def generate_unique_code(session: Session, length: int | None = None) -> str:
    """Erzeugt einen Kurzcode, der noch nicht in der Datenbank vergeben ist."""
    code = generate_code(length)
    while code_exists(session, code):
        code = generate_code(length)
    return code
