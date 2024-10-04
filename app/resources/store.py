import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.db import stores
from app.schemas.store import StoreSchema

store_blp = Blueprint("stores", __name__, description="APIs to manage stores")


@store_blp.route("/stores")
class Stores(MethodView):
    @store_blp.arguments(StoreSchema)
    @store_blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(400, error="Store already exists")
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201

    @store_blp.response(200, StoreSchema(many=True))
    def get(self):
        return list(stores.values())


@store_blp.route("/stores/<store_id>")
class StoresById(MethodView):
    @store_blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, error="Store not found")

    @store_blp.arguments(StoreSchema)
    @store_blp.response(200, StoreSchema)
    def patch(self, store_data, store_id):
        try:
            store = stores[store_id]
            store |= store_data
            return store
        except KeyError:
            abort(404, error="Store not found")

    @store_blp.response(204)
    def delete(self, store_id):
        try:
            del stores[store_id]
            return "", 204
        except KeyError:
            abort(404, error="Store not found")
