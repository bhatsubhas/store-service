from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from app.db import db
from app.models.item import ItemModel
from app.schemas.item import ItemSchema, ItemUpdateSchema

item_blp = Blueprint("items", __name__, description="APIs to manage items")


@item_blp.route("/items")
class Items(MethodView):
    @item_blp.arguments(ItemSchema)
    @item_blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500, error="An internal error occurred while inserting the item"
            )
        return item, 201

    @item_blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()


@item_blp.route("/items/<item_id>")
class ItemsById(MethodView):
    @item_blp.response(200, ItemSchema)
    def get(self, item_id):
        return ItemModel.query.get_or_404(item_id)

    @item_blp.arguments(ItemUpdateSchema)
    @item_blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

    @item_blp.response(204)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
