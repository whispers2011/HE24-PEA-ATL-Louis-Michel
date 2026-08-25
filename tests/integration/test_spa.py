"""Auslieferung des gebauten Frontends (SPA) unter /app."""

from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import settings
from app.main import mount_frontend


@pytest.fixture(name="spa_client")
def spa_client_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """App mit gebautem Frontend in einem temporären dist-Verzeichnis."""
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<html><body>SPA</body></html>")
    (dist / "assets" / "app.js").write_text("console.log('spa')")
    monkeypatch.setattr(settings, "frontend_dist", str(dist))
    app = FastAPI()
    mount_frontend(app)
    return TestClient(app)


def test_spa_index_is_served(spa_client):
    resp = spa_client.get("/app/")
    assert resp.status_code == 200
    assert "SPA" in resp.text


def test_spa_assets_are_served(spa_client):
    resp = spa_client.get("/app/assets/app.js")
    assert resp.status_code == 200


def test_unknown_spa_route_falls_back_to_index(spa_client):
    """Deep-Links des History-Routers liefern die index.html aus."""
    resp = spa_client.get("/app/links")
    assert resp.status_code == 200
    assert "SPA" in resp.text


def test_non_get_methods_are_rejected(spa_client):
    resp = spa_client.post("/app/index.html")
    assert resp.status_code == 405


def test_root_redirects_to_spa(spa_client):
    resp = spa_client.get("/", follow_redirects=False)
    assert resp.status_code == 307
    assert resp.headers["location"] == "/app/"


def test_without_frontend_dist_nothing_is_mounted():
    app = FastAPI()
    mount_frontend(app)
    client = TestClient(app)
    assert client.get("/app/").status_code == 404
    assert client.get("/").status_code == 404
