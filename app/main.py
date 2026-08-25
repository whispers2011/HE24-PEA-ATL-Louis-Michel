"""FastAPI-Anwendung des URL-Shorteners."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response
from starlette.types import Scope

from app.config import settings
from app.database import init_db
from app.routers import auth, links, redirect, stats


class SPAStaticFiles(StaticFiles):
    """Statische Dateien mit index.html-Fallback für Client-Routen der SPA."""

    async def get_response(self, path: str, scope: Scope) -> Response:
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            if exc.status_code != 404:
                raise
            # Unbekannter Pfad = Route des History-Routers: die SPA übernimmt.
            return await super().get_response("index.html", scope)


def mount_frontend(app: FastAPI) -> None:
    """Bindet das gebaute Frontend unter /app ein, wenn FRONTEND_DIST gesetzt ist."""
    if not settings.frontend_dist:
        return

    @app.get("/", include_in_schema=False)
    def frontend_root() -> RedirectResponse:
        return RedirectResponse(url="/app/")

    app.mount(
        "/app",
        SPAStaticFiles(directory=settings.frontend_dist, html=True),
        name="frontend",
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialisiert beim Start die Datenbanktabellen."""
    init_db()
    yield


app = FastAPI(title="URL-Shortener", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Liefert den Betriebszustand fuer Monitoring und CI."""
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(links.router)
app.include_router(stats.router)
# Das SPA-Mount muss vor dem Catch-all stehen, damit /app nie als Kurzcode gilt.
mount_frontend(app)
# Catch-all-Weiterleitung zuletzt registrieren, damit spezifische Routen
# (z. B. /health, /docs, /app, /api/...) Vorrang vor `GET /{code}` haben.
app.include_router(redirect.router)
