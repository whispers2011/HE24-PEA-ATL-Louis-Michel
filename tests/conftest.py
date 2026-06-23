import os

# Test-Signaturschlüssel setzen, bevor app-Module die Settings laden.
# Nur für die Testumgebung – kein Produktiv-Secret.
os.environ.setdefault("SECRET_KEY", "testing-secret-key-not-for-production-use")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402
from sqlmodel import Session, SQLModel, create_engine  # noqa: E402

from app.database import get_session  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(name="memory_engine")
def memory_engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield engine
    engine.dispose()


@pytest.fixture(name="session")
def session_fixture(memory_engine):
    SQLModel.metadata.create_all(memory_engine)
    with Session(memory_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="make_auth")
def make_auth_fixture(client):
    """Registriert einen Benutzer und liefert dessen Bearer-Header."""

    def _make(
        email: str = "owner@example.com", password: str = "secret123"
    ) -> dict[str, str]:
        client.post("/api/auth/register", json={"email": email, "password": password})
        resp = client.post(
            "/api/auth/login", data={"username": email, "password": password}
        )
        return {"Authorization": f"Bearer {resp.json()['access_token']}"}

    return _make
