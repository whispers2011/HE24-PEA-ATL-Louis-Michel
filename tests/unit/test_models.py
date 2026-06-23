from datetime import datetime

from sqlmodel import Session, select

from app.models import Click, Link, User


def _make_user(session: Session, email: str = "a@example.com") -> User:
    user = User(email=email, hashed_password="x")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_relationships_link_back_to_owner_and_clicks(session: Session):
    user = _make_user(session)
    link = Link(code="abc123", target_url="https://example.com", owner_id=user.id)
    session.add(link)
    session.commit()
    click = Click(link_id=link.id)
    session.add(click)
    session.commit()
    session.refresh(user)
    session.refresh(link)

    assert link.owner == user
    assert link in user.links
    assert click.link == link
    assert click in link.clicks


def test_created_at_is_set_automatically(session: Session):
    user = _make_user(session)
    assert isinstance(user.created_at, datetime)


def test_email_is_unique(session: Session):
    _make_user(session, "dup@example.com")
    session.add(User(email="dup@example.com", hashed_password="y"))
    try:
        session.commit()
    except Exception:
        session.rollback()
    else:  # pragma: no cover
        raise AssertionError("doppelte E-Mail haette einen Fehler ausloesen muessen")


def test_deleting_link_removes_its_clicks(session: Session):
    user = _make_user(session)
    link = Link(code="del001", target_url="https://example.com", owner_id=user.id)
    session.add(link)
    session.commit()
    session.add(Click(link_id=link.id))
    session.commit()

    session.delete(link)
    session.commit()

    assert session.exec(select(Click)).all() == []
