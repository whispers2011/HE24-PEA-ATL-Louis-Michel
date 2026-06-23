"""FastAPI-Anwendung des URL-Shorteners."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialisiert beim Start die Datenbanktabellen."""
    init_db()
    yield


app = FastAPI(title="URL-Shortener", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    """Liefert den Betriebszustand fuer Monitoring und CI."""
    return {"status": "ok"}
