def _create_link(client, headers, target: str = "https://example.com") -> str:
    return client.post(
        "/api/links", json={"target_url": target}, headers=headers
    ).json()["code"]


def test_stats_counts_clicks_for_own_link(client, make_auth):
    headers = make_auth()
    code = _create_link(client, headers)
    client.get(f"/{code}", follow_redirects=False)
    client.get(f"/{code}", follow_redirects=False)

    resp = client.get(f"/api/links/{code}/stats", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["code"] == code
    assert body["total"] == 2
    assert sum(body["per_day"].values()) == 2


def test_stats_for_link_without_clicks_is_zero(client, make_auth):
    headers = make_auth()
    code = _create_link(client, headers)
    resp = client.get(f"/api/links/{code}/stats", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["total"] == 0
    assert resp.json()["per_day"] == {}


def test_stats_requires_authentication(client, make_auth):
    headers = make_auth()
    code = _create_link(client, headers)
    resp = client.get(f"/api/links/{code}/stats")
    assert resp.status_code == 401


def test_stats_unknown_link_returns_404(client, make_auth):
    headers = make_auth()
    resp = client.get("/api/links/missing/stats", headers=headers)
    assert resp.status_code == 404


def test_stats_foreign_link_returns_403(client, make_auth):
    owner = make_auth("owner@example.com")
    other = make_auth("other@example.com")
    code = _create_link(client, owner)
    resp = client.get(f"/api/links/{code}/stats", headers=other)
    assert resp.status_code == 403
