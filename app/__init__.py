import os

from flask import Flask
from flask_smorest import Api, abort

from app.config import DevConfig, ProdConfig
from app.db import db
from app.resources.healthz import healthz_blp
from app.resources.item import item_blp
from app.resources.store import store_blp


def create_app():
    app = Flask(__name__)
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(healthz_blp)
    api.register_blueprint(store_blp)
    api.register_blueprint(item_blp)
    return app
