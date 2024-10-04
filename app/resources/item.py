import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.db import items, stores
from app.schemas.item import ItemSchema, ItemUpdateSchema

item_blp = Blueprint("items", __name__, description="APIs to manage items")


@item_blp.route("/items")
class Items(MethodView):
    @item_blp.arguments(ItemSchema)
    @item_blp.response(201, ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if (
                item["name"] == item_data["name"]
                and item["store_id"] == item_data["store_id"]
            ):
                abort(400, error="Item already exists")

        if item_data["store_id"] not in stores:
            abort(404, error="Store not found")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201

    @item_blp.response(200, ItemSchema(many=True))
    def get(self):
        return list(items.values())


@item_blp.route("/items/<item_id>")
class ItemsById(MethodView):
    @item_blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, error="Item not found")

    @item_blp.arguments(ItemUpdateSchema)
    @item_blp.response(200, ItemSchema)
    def patch(self, item_data, item_id):
        print(item_data)
        if not ("name" in item_data or "price" in item_data):
            abort(400, error="Either 'name' or 'price' must be present")

        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, error="Item not found")

    @item_blp.response(204)
    def delete(self, item_id):
        try:
            del items[item_id]
            return "", 204
        except KeyError:
            abort(404, error="Item not found")
