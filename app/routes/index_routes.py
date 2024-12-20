from flask import Blueprint, redirect, url_for
from flask_login import current_user

from app.components.layout.navbar_component import navbar_component
from app.components.layout.footer_component import footer_component
from app.routes import render_page

index_routes = Blueprint("index", __name__)


@index_routes.route("/", methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

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
