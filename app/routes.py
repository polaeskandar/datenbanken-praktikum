from flask import render_template, Blueprint

from app.components.navbar_component import navbar_component
from app.components.footer_component import footer_component
from app.components.order_history_component import order_history_component

routes_blueprint = Blueprint("routes", __name__)


@routes_blueprint.route("/", methods=["GET", "POST"])
def index():
    components = {
        "header": [
            navbar_component(),
        ],
        "main": [
            order_history_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_template(
        "layout.html",
        components=components,
        page_title="Home",
    )
