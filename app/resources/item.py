import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..db import items, stores

item_blp = Blueprint("items", __name__, description="APIs to manage items")


@item_blp.route("/items")
class Items(MethodView):
    def post(self):
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

    def get(self):
        return {"items": list(items.values())}


@item_blp.route("/items/<item_id>")
class ItemsById(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, error="Item not found")

    def patch(self, item_id):
        item_data = request.get_json()
        if "name" not in item_data or "price" not in item_data:
            abort(400, error="Either 'name' or 'price' must be present")

        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, error="Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return "", 204
        except KeyError:
            abort(404, error="Item not found")
