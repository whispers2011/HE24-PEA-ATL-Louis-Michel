"""FastAPI-Anwendung des URL-Shorteners."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import auth, links


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialisiert beim Start die Datenbanktabellen."""
    init_db()
    yield


app = FastAPI(title="URL-Shortener", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(links.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Liefert den Betriebszustand fuer Monitoring und CI."""
    return {"status": "ok"}
