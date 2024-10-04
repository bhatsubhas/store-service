import os

from flask import Flask
from flask_smorest import Api

from .config import DevConfig, ProdConfig
from .resources.healthz import healthz_blp
from .resources.item import item_blp
from .resources.store import store_blp

app = Flask(__name__)
if os.environ.get("FLASK_ENV") == "production":
    app.config.from_object(ProdConfig)
else:
    app.config.from_object(DevConfig)
api = Api(app)
api.register_blueprint(healthz_blp)
api.register_blueprint(store_blp)
api.register_blueprint(item_blp)
