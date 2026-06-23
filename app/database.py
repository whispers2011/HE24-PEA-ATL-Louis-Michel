"""Datenbank-Engine, Tabellen-Initialisierung und Session-Bereitstellung."""

from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app import models  # noqa: F401  – registriert die Tabellen in SQLModel.metadata
from app.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)


def init_db() -> None:
    """Legt alle in SQLModel.metadata registrierten Tabellen an."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session]:
    """Stellt eine Datenbank-Session als FastAPI-Dependency bereit."""
    with Session(engine) as session:
        yield session
