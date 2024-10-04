from flask import Config


class CommonConfig(Config):
    API_TITLE = "Stores API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/api/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc-ui"
    OPENAPI_RAPIDOC_URL = (
        "https://cdn.jsdelivr.net/npm/rapidoc/dist/rapidoc-min.js"
    )


class DevConfig(CommonConfig):
    DEBUG = True
    SECRET_KEY = "this-is-top-secret"


class ProdConfig(CommonConfig):
    pass
