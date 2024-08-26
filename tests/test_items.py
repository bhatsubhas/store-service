def test_get_items_list(client):
    response = client.get("/items")
    assert response.status_code == 200

    items = response.get_json()["items"]
    assert isinstance(items, list)


def test_post_item(client):
    item_data = {"name": "Table", "price": 1299, "store_id": "1"}
    response = client.post("/items", json=item_data)
    assert response.status_code == 201

    item = response.get_json()
    assert (
        item["item_id"] is not None
        and item["name"] == "Table"
        and item["price"] == 1299
    )

    item_data = {"name": "Table", "price": 1299, "store_id": "2"}
    response = client.post("/items", json=item_data)
    assert response.status_code == 404

    error = response.get_json()
    assert error["error"] == "STORE_NOT_FOUND"


def test_get_item(client):
    item_id = "1"
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200

    item = response.get_json()
    assert (
        item["item_id"] == "1"
        and item["store_id"] == "1"
        and item["name"] == "Chair"
        and item["price"] == 1299
    )

    item_id = "3"
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404

    error = response.get_json()
    assert error["error"] == "ITEM_NOT_FOUND"
