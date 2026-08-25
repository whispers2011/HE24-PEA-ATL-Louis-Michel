from fastapi.testclient import TestClient

import app.database as database
from app.main import app


def test_health_returns_ok(client):
    response = client.get("/health")

    # Bewusst falsche Erwartung: Nachweis, dass Cloud Build bei einem
    # fehlgeschlagenen Test abbricht und nichts deployed (ATL #2, Abschnitt 7.4).
    assert response.status_code == 418
    assert response.json() == {"status": "ok"}


def test_lifespan_starts_and_serves(monkeypatch, memory_engine):
    monkeypatch.setattr(database, "engine", memory_engine)

    with TestClient(app) as started_client:
        response = started_client.get("/health")

    assert response.status_code == 200
