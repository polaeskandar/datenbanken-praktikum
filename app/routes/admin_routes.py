from flask import Blueprint, Response

from app.components.admin.aside_menu_component import aside_menu_component
from app.components.admin.edit_settings_component import edit_settings_component
from app.components.admin.get_delivery_radius_component import (
    get_delivery_radius_component,
)
from app.components.admin.menu_page_navigation_component import (
    menu_page_navigation_component,
)
from app.components.admin.orders_table_component import orders_table_component
from app.components.admin.set_delivery_radius_component import delivery_radius_component
from app.components.admin.set_opening_hours_component import set_opening_hours_component
from app.components.footer_component import footer_component
from app.components.navbar_component import navbar_component
from app.routes import render_page

admin_routes = Blueprint("admin", __name__)


@admin_routes.route("/")
@admin_routes.route("/orders")
def index() -> Response:
    components = {
        "header": [
            navbar_component(),
        ],
        "aside": [
            aside_menu_component(),
        ],
        "main": [
            orders_table_component(),
        ],
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
            set_opening_hours_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("admin.html", "Opening Hours", components)


@admin_routes.route("/delivery_radius", methods=["GET", "POST"])
def delivery_radius() -> Response:
    components = {
        "header": [
            navbar_component(),
        ],
        "aside": [
            aside_menu_component(),
        ],
        "main": [
            delivery_radius_component(),
            get_delivery_radius_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("admin.html", "Delivery Radius", components)


@admin_routes.route("/settings", methods=["GET", "POST"])
def settings() -> Response:
    components = {
        "header": [
            navbar_component(),
        ],
        "aside": [
            aside_menu_component(),
        ],
        "main": [
            edit_settings_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("admin.html", "Settings", components)
