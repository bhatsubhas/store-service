from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app import db
from app.db import stores
from app.models.store import StoreModel
from app.schemas.store import BaseStoreSchema, StoreSchema

store_blp = Blueprint("stores", __name__, description="APIs to manage stores")


@store_blp.route("/stores")
class Stores(MethodView):
    @store_blp.arguments(BaseStoreSchema)
    @store_blp.response(201, BaseStoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            print("Got integrity error")
            abort(400, error="A store with given name already exists")
        except SQLAlchemyError:
            abort(
                500,
                error="An internal error occurred while inserting the store",
            )
        return store, 201

    @store_blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()


@store_blp.route("/stores/<store_id>")
class StoresById(MethodView):
    @store_blp.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)

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
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
