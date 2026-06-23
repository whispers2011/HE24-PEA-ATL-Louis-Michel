from datetime import UTC, datetime, timedelta

import jwt

from app.config import settings
from app.security import ALGORITHM, create_access_token


def _bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_register_returns_created_user_without_password(client):
    resp = client.post(
        "/api/auth/register",
        json={"email": "a@example.com", "password": "secret123"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "a@example.com"
    assert "hashed_password" not in body
    assert "password" not in body


def test_register_duplicate_email_conflicts(client):
    payload = {"email": "dup@example.com", "password": "secret123"}
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_returns_bearer_token(client):
    client.post(
        "/api/auth/register",
        json={"email": "a@example.com", "password": "secret123"},
    )
    resp = client.post(
        "/api/auth/login",
        data={"username": "a@example.com", "password": "secret123"},
    )
    assert resp.status_code == 200
    assert resp.json()["token_type"] == "bearer"
    assert resp.json()["access_token"]


def test_login_wrong_password_unauthorized(client):
    client.post(
        "/api/auth/register",
        json={"email": "a@example.com", "password": "secret123"},
    )
    resp = client.post(
        "/api/auth/login",
        data={"username": "a@example.com", "password": "wrong"},
    )
    assert resp.status_code == 401


def test_login_unknown_email_unauthorized(client):
    resp = client.post(
        "/api/auth/login",
        data={"username": "ghost@example.com", "password": "x"},
    )
    assert resp.status_code == 401


def test_me_returns_current_user(client, make_auth):
    headers = make_auth("me@example.com")
    resp = client.get("/api/auth/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@example.com"


def test_me_without_token_unauthorized(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_me_with_invalid_token_unauthorized(client):
    resp = client.get("/api/auth/me", headers=_bearer("not-a-jwt"))
    assert resp.status_code == 401


def test_me_with_expired_token_unauthorized(client):
    expired = jwt.encode(
        {"sub": "a@example.com", "exp": datetime.now(UTC) - timedelta(minutes=1)},
        settings.secret_key,
        algorithm=ALGORITHM,
    )
    resp = client.get("/api/auth/me", headers=_bearer(expired))
    assert resp.status_code == 401


def test_me_with_token_without_subject_unauthorized(client):
    token = jwt.encode(
        {"exp": datetime.now(UTC) + timedelta(minutes=5)},
        settings.secret_key,
        algorithm=ALGORITHM,
    )
    resp = client.get("/api/auth/me", headers=_bearer(token))
    assert resp.status_code == 401


def test_me_with_unknown_subject_unauthorized(client):
    token = create_access_token("ghost@example.com")
    resp = client.get("/api/auth/me", headers=_bearer(token))
    assert resp.status_code == 401
