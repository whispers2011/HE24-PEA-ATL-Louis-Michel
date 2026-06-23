import pytest
from sqlmodel import Session

from app.config import settings
from app.models import Link, User
from app.services import shortcode


def _store_link_with_code(session: Session, code: str) -> None:
    user = User(email=f"{code}@example.com", hashed_password="x")
    session.add(user)
    session.commit()
    session.refresh(user)
    session.add(Link(code=code, target_url="https://example.com", owner_id=user.id))
    session.commit()


def test_generate_code_has_requested_length():
    assert len(shortcode.generate_code(8)) == 8


def test_generate_code_uses_configured_length_by_default():
    assert len(shortcode.generate_code()) == settings.code_length


def test_generate_code_uses_only_allowed_alphabet():
    code = shortcode.generate_code(64)
    assert set(code) <= set(shortcode.ALPHABET)


@pytest.mark.parametrize("alias", ["abc", "my-link_1", "A1b2C3"])
def test_valid_aliases_are_accepted(alias: str):
    assert shortcode.is_valid_alias(alias) is True


@pytest.mark.parametrize(
    "alias",
    ["ab", "with space", "bad!char", "", "a" * 33],
)
def test_invalid_aliases_are_rejected(alias: str):
    assert shortcode.is_valid_alias(alias) is False


def test_generate_unique_code_returns_unused_code(session: Session):
    code = shortcode.generate_unique_code(session)
    assert shortcode.code_exists(session, code) is False


def test_generate_unique_code_retries_on_collision(session: Session, monkeypatch):
    _store_link_with_code(session, "TAKEN1")
    candidates = iter(["TAKEN1", "FRESH2"])
    monkeypatch.setattr(
        shortcode, "generate_code", lambda length=None: next(candidates)
    )
    assert shortcode.generate_unique_code(session) == "FRESH2"
