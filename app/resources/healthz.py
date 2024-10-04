from flask.views import MethodView
from flask_smorest import Blueprint

healthz_blp = Blueprint(
    "healthz", __name__, description="APIs to manage service health"
)


@healthz_blp.route("/healthz/status")
class Healthz(MethodView):
    def get(self):
        return {"message": "stores service status is healthy"}
