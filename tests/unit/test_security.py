import jwt

from app.config import settings
from app.security import (
    ALGORITHM,
    create_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_is_not_plaintext_and_verifies():
    hashed = hash_password("secret123")
    assert hashed != "secret123"
    assert verify_password("secret123", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("secret123")
    assert verify_password("wrong", hashed) is False


def test_create_access_token_encodes_subject_and_expiry():
    token = create_access_token("user@example.com")
    payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    assert payload["sub"] == "user@example.com"
    assert "exp" in payload
