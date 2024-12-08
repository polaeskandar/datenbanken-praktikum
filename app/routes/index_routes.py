from flask import render_template, Blueprint

from app.components.navbar_component import navbar_component
from app.components.footer_component import footer_component
from app.routes import render_page

index_routes = Blueprint("index", __name__)


@index_routes.route("/", methods=["GET", "POST"])
def index():
    components = {
        "header": [
            navbar_component(),
        ],
        "main": [],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("layout.html", "Home", components)
