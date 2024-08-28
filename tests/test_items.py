def test_get_items_list(client):
    response = client.get("/items")
    assert response.status_code == 200

    items = response.get_json()["items"]
    assert isinstance(items, list)


def test_post_item(client):
    item_data = {"name": "Compact Disc", "price": 1299, "store_id": "1"}
    response = client.post("/items", json=item_data)
    assert response.status_code == 201

    item = response.get_json()
    assert (
        item["item_id"] is not None
        and item["name"] == "Compact Disc"
        and item["price"] == 1299
    )

    item_data = {"name": "Table", "price": 1299, "store_id": "2"}
    response = client.post("/items", json=item_data)
    assert response.status_code == 404

    # error = response.get_json()
    # assert error["error"] == "STORE_NOT_FOUND"

    item_data = {"name": "Chair", "price": 1299, "store_id": "1"}
    response = client.post("/items", json=item_data)
    assert response.status_code == 400

    item_data = {"name": "Chair", "price": 1299}
    response = client.post("/items", json=item_data)
    assert response.status_code == 400


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

    # error = response.get_json()
    # assert error["error"] == "ITEM_NOT_FOUND"


def test_update_item(client):
    item_id = "1"
    item_data = {"name": "Premium Chair", "price": 1399}
    response = client.patch(f"/items/{item_id}", json=item_data)
    assert response.status_code == 200

    item = response.get_json()
    assert (
        item["item_id"] == "1"
        and item["name"] == "Premium Chair"
        and item["price"] == 1399
    )

    item_id = "1"
    item_data = {"name": "Premium Chair"}
    response = client.patch(f"/items/{item_id}", json=item_data)
    assert response.status_code == 400

    item_id = "1234"
    item_data = {"name": "Premium Chair", "price": 1399}
    response = client.patch(f"/items/{item_id}", json=item_data)
    assert response.status_code == 404


def test_delete_item(client):
    item_id = "1"
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204

    item_id = "1234"
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 404
