from flask import render_template, Blueprint

from app.components.navbar_component import navbar_component

routes_blueprint = Blueprint("routes", __name__)


@routes_blueprint.route("/", methods=["GET", "POST"])
def index():
    components = {
        "header": [
            navbar_component(),
        ],
        "main": [],
        "footer": [],
    }

    return render_template(
        "layout.html",
        components=components,
        page_title="Home",
    )
