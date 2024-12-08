from flask import Blueprint, Response

from app.components.admin.aside_menu_component import aside_menu_component
from app.components.admin.opening_times_component import opening_times_component
from app.components.footer_component import footer_component
from app.components.navbar_component import navbar_component
from app.routes import render_page

admin_routes = Blueprint("admin", __name__)


@admin_routes.route("/")
def index() -> Response:
    components = {
        "header": [
            navbar_component(),
        ],
        "aside": [
            aside_menu_component(),
        ],
        "main": [],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("admin.html", "Admin", components)


@admin_routes.route("/opening-hours", methods=["GET", "POST"])
def opening_hours() -> Response:
    components = {
        "header": [
            navbar_component(),
        ],
        "aside": [
            aside_menu_component(),
        ],
        "main": [
            opening_times_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("admin.html", "Opening Hours", components)
