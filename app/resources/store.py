import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..db import stores

store_blp = Blueprint("stores", __name__, description="APIs to manage stores")


@store_blp.route("/stores")
class Stores(MethodView):
    def post(self):
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

    def get(self):
        return {"stores": list(stores.values())}


@store_blp.route("/stores/<store_id>")
class StoresById(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, error="Store not found")

    def patch(self, store_id):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(400, error="'name' must be present")

        try:
            store = stores[store_id]
            store |= store_data
            return store
        except KeyError:
            abort(404, error="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return "", 204
        except KeyError:
            abort(404, error="Store not found")
