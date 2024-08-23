def test_get_items_list(client):
    store_name = "My Store"
    response = client.get(f"/stores/{store_name}/items")
    assert response.status_code == 200

    items = response.get_json()["items"]
    assert isinstance(items, list)

    store_name = "Unknown"
    response = client.get(f"/stores/{store_name}/items")
    assert response.status_code == 404

    error = response.get_json()
    assert error["error"] == "STORE_NOT_FOUND"


def test_post_item(client):
    store_name = "My Store"
    item_data = {"name": "Table", "price": 1299}
    response = client.post(f"/stores/{store_name}/items", json=item_data)
    assert response.status_code == 201

    item = response.get_json()
    assert item["name"] == "Table" and item["price"] == 1299

    store_name = "Unknown"
    response = client.post(f"/stores/{store_name}/items", json=item_data)
    assert response.status_code == 404

    error = response.get_json()
    assert error["error"] == "STORE_NOT_FOUND"
