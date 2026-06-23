"""SQLModel-Tabellen des URL-Shorteners: User, Link und Click."""

from datetime import UTC, datetime

from sqlmodel import Field, Relationship, SQLModel


def utcnow() -> datetime:
    """Aktueller Zeitpunkt in UTC – Standardwert der created_at-Spalten."""
    return datetime.now(UTC)


class User(SQLModel, table=True):
    """Registrierter Benutzer; besitzt beliebig viele Kurzlinks."""

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=utcnow)

    links: list["Link"] = Relationship(back_populates="owner", cascade_delete=True)


class Link(SQLModel, table=True):
    """Kurzlink eines Benutzers; sammelt seine Klicks."""

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    target_url: str
    owner_id: int = Field(foreign_key="user.id", index=True, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=utcnow)

    owner: User | None = Relationship(back_populates="links")
    clicks: list["Click"] = Relationship(back_populates="link", cascade_delete=True)


class Click(SQLModel, table=True):
    """Einzelner Aufruf eines Kurzlinks mit Zeitstempel."""

    id: int | None = Field(default=None, primary_key=True)
    link_id: int = Field(foreign_key="link.id", index=True, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=utcnow)

    link: Link | None = Relationship(back_populates="clicks")
