from sqlmodel import Session, select

from app.models import Click


def _create_link(client, make_auth, target: str = "https://example.com/dest") -> str:
    headers = make_auth()
    resp = client.post("/api/links", json={"target_url": target}, headers=headers)
    return resp.json()["code"]


def test_redirect_returns_307_to_target(client, make_auth):
    code = _create_link(client, make_auth)
    resp = client.get(f"/{code}", follow_redirects=False)
    assert resp.status_code == 307
    assert resp.headers["location"].startswith("https://example.com/dest")


def test_redirect_is_public(client, make_auth):
    code = _create_link(client, make_auth)
    # kein Authorization-Header – Weiterleitung muss trotzdem funktionieren
    resp = client.get(f"/{code}", follow_redirects=False)
    assert resp.status_code == 307


def test_redirect_unknown_code_returns_404(client):
    resp = client.get("/does-not-exist", follow_redirects=False)
    assert resp.status_code == 404


def test_redirect_records_one_click_per_request(client, make_auth, session: Session):
    code = _create_link(client, make_auth)
    client.get(f"/{code}", follow_redirects=False)
    client.get(f"/{code}", follow_redirects=False)
    assert len(session.exec(select(Click)).all()) == 2
