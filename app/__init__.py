import uuid
from flask import Flask, request
from flask_smorest import abort
from .db import stores, items


app = Flask(__name__)


@app.get("/healthz/status")
def health_check():
    return {"message": "service status is healthy"}


@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/stores")
def create_stores():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, error="'name' is mandatory")

    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, error="Store already exists")
    store_id = uuid.uuid4().hex
    store = {**store_data, "store_id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/items")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "name" not in item_data
        or "store_id" not in item_data
    ):
        abort(400, error="'price', 'name' and 'store_id' are mandatory")

    for item in items.values():
        if (
            item["name"] == item_data["name"]
            and item["store_id"] == item_data["store_id"]
        ):
            abort(400, error="Item already exists")

    if item_data["store_id"] not in stores:
        abort(404, error="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "item_id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/stores/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, error="Store not found")


@app.patch("/stores/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, "'name' must be present")

    try:
        store = stores[store_id]
        store |= store_data
        return store
    except KeyError:
        abort(404, error="Store not found")


@app.delete("/stores/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return "", 204
    except KeyError:
        abort(404, error="Store not found")


@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/items/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, error="Item not found")


@app.patch("/items/<string:item_id>")
def udpate_item(item_id):
    item_data = request.get_json()
    if "name" not in item_data or "price" not in item_data:
        abort(400, "Either 'name' or 'price' must be present")

    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, error="Item not found")


@app.delete("/items/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return "", 204
    except KeyError:
        abort(404, error="Item not found")
