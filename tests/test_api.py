import json


def test_root_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert data.get("message") == "Business Search API"


def test_health_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data.get("status") == "ok"
    assert isinstance(data.get("count"), int)


def test_search_post_basic(client):
    payload = {"query": "affordable housing near 94103", "page": 1, "limit": 5}
    res = client.post("/api/search", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 200
    data = res.get_json()
    assert data.get("success") is True
    assert isinstance(data.get("results"), list)
    assert "total_found" in data


def test_search_get_passthrough(client):
    res = client.get("/search?q=housing&zip=94103&radius=10&cause=housing")
    assert res.status_code == 200
    data = res.get_json()
    assert data.get("success") is True
    assert isinstance(data.get("results"), list)


