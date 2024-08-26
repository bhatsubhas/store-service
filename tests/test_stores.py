def test_get_stores_list(client):
    response = client.get("/stores")
    assert response.status_code == 200

    stores = response.get_json()["stores"]
    assert isinstance(stores, list) and len(stores) >= 0


def test_get_store(client):
    store_id = "1"
    response = client.get(f"/stores/{store_id}")
    assert response.status_code == 200

    store = response.get_json()
    assert store["store_id"] == store_id
    assert store["name"] == "My Store"

    store_id = "Unknown"
    response = client.get(f"/stores/{store_id}")
    assert response.status_code == 404

    error = response.get_json()
    assert error["error"] == "STORE_NOT_FOUND"


def test_create_store(client):
    request_body = {"name": "Test Store"}
    response = client.post("/stores", json=request_body)
    assert response.status_code == 201

    store = response.get_json()
    assert store["name"] == "Test Store"
    assert store["store_id"] is not None
