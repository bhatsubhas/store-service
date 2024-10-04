def test_get_stores_list(client):
    response = client.get("/stores")
    assert response.status_code == 200

    stores = response.get_json()
    assert isinstance(stores, list) and len(stores) >= 0


def test_get_store(client):
    store_id = "1"
    response = client.get(f"/stores/{store_id}")
    assert response.status_code == 200

    store = response.get_json()
    assert store["id"] == store_id
    assert store["name"] == "My Store"

    store_id = "Unknown"
    response = client.get(f"/stores/{store_id}")
    assert response.status_code == 404

    # error = response.get_json()
    # assert error["error"] == "STORE_NOT_FOUND"


def test_create_store(client):
    request_body = {"name": "Test Store"}
    response = client.post("/stores", json=request_body)
    assert response.status_code == 201

    store = response.get_json()
    assert store["name"] == "Test Store"
    assert store["id"] is not None

    request_body = {}
    response = client.post("/stores", json=request_body)
    assert response.status_code == 422

    request_body = {"name": "My Store"}
    response = client.post("/stores", json=request_body)
    assert response.status_code == 400


def test_update_store(client):
    store_id = "1"
    store_data = {"name": "My Premium Store"}
    response = client.patch(f"/stores/{store_id}", json=store_data)
    assert response.status_code == 200

    item = response.get_json()
    assert item["id"] == "1" and item["name"] == "My Premium Store"

    store_id = "1"
    store_data = {}
    response = client.patch(f"/stores/{store_id}", json=store_data)
    assert response.status_code == 422

    store_id = "1234"
    store_data = {"name": "My Premium Store"}
    response = client.patch(f"/stores/{store_id}", json=store_data)
    assert response.status_code == 404


def test_delete_store(client):
    store_id = "1"
    response = client.delete(f"/stores/{store_id}")
    assert response.status_code == 204

    store_id = "1234"
    response = client.delete(f"/stores/{store_id}")
    assert response.status_code == 404
