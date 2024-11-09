from marshmallow import fields

from app.schemas.item import BaseItemSchema, BaseStoreSchema


class StoreSchema(BaseStoreSchema):
    items = fields.List(fields.Nested(BaseItemSchema(), dump_only=True))
