def test_create_link_generates_code(client, make_auth):
    headers = make_auth()
    resp = client.post(
        "/api/links", json={"target_url": "https://example.com"}, headers=headers
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["code"]
    assert body["short_url"].endswith(body["code"])
    assert body["target_url"].startswith("https://example.com")
    assert "created_at" in body


def test_create_link_with_valid_alias(client, make_auth):
    headers = make_auth()
    resp = client.post(
        "/api/links",
        json={"target_url": "https://example.com", "alias": "my-alias"},
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["code"] == "my-alias"


def test_create_link_invalid_alias_returns_400(client, make_auth):
    headers = make_auth()
    resp = client.post(
        "/api/links",
        json={"target_url": "https://example.com", "alias": "no good!"},
        headers=headers,
    )
    assert resp.status_code == 400


def test_create_link_duplicate_alias_returns_409(client, make_auth):
    headers = make_auth()
    payload = {"target_url": "https://example.com", "alias": "taken"}
    client.post("/api/links", json=payload, headers=headers)
    resp = client.post("/api/links", json=payload, headers=headers)
    assert resp.status_code == 409


def test_create_link_rejects_non_http_url_422(client, make_auth):
    headers = make_auth()
    resp = client.post(
        "/api/links", json={"target_url": "ftp://example.com"}, headers=headers
    )
    assert resp.status_code == 422


def test_create_link_requires_authentication(client):
    resp = client.post("/api/links", json={"target_url": "https://example.com"})
    assert resp.status_code == 401


def test_list_returns_only_own_links(client, make_auth):
    owner = make_auth("owner@example.com")
    other = make_auth("other@example.com")
    client.post("/api/links", json={"target_url": "https://a.com"}, headers=owner)
    client.post("/api/links", json={"target_url": "https://b.com"}, headers=owner)
    client.post("/api/links", json={"target_url": "https://c.com"}, headers=other)

    resp = client.get("/api/links", headers=owner)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_own_link(client, make_auth):
    headers = make_auth()
    code = client.post(
        "/api/links", json={"target_url": "https://example.com"}, headers=headers
    ).json()["code"]
    resp = client.get(f"/api/links/{code}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == code


def test_get_unknown_link_returns_404(client, make_auth):
    headers = make_auth()
    resp = client.get("/api/links/missing", headers=headers)
    assert resp.status_code == 404


def test_get_foreign_link_returns_403(client, make_auth):
    owner = make_auth("owner@example.com")
    other = make_auth("other@example.com")
    code = client.post(
        "/api/links", json={"target_url": "https://a.com"}, headers=owner
    ).json()["code"]
    resp = client.get(f"/api/links/{code}", headers=other)
    assert resp.status_code == 403


def test_delete_own_link(client, make_auth):
    headers = make_auth()
    code = client.post(
        "/api/links", json={"target_url": "https://example.com"}, headers=headers
    ).json()["code"]
    resp = client.delete(f"/api/links/{code}", headers=headers)
    assert resp.status_code == 204
    assert client.get(f"/api/links/{code}", headers=headers).status_code == 404


def test_delete_unknown_link_returns_404(client, make_auth):
    headers = make_auth()
    resp = client.delete("/api/links/missing", headers=headers)
    assert resp.status_code == 404


def test_delete_foreign_link_returns_403(client, make_auth):
    owner = make_auth("owner@example.com")
    other = make_auth("other@example.com")
    code = client.post(
        "/api/links", json={"target_url": "https://a.com"}, headers=owner
    ).json()["code"]
    resp = client.delete(f"/api/links/{code}", headers=other)
    assert resp.status_code == 403
