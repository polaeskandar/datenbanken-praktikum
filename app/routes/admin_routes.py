from flask import Blueprint, Response, abort, flash, redirect, url_for
from flask_login import current_user

from app import app, db
from app.components.admin.menu.add_menu_item_component import add_menu_item_component
from app.components.admin.aside_menu_component import aside_menu_component
from app.components.admin.menu.edit_menu_item_component import edit_menu_item_component
from app.components.admin.edit_settings_component import edit_settings_component
from app.components.admin.get_delivery_radius_component import (
    get_delivery_radius_component,
)
from app.components.admin.menu.menu_overview_component import menu_overview_component
from app.components.admin.menu.menu_page_navigation_component import (
    menu_page_navigation_component,
)
from app.components.admin.orders_table_component import orders_table_component
from app.components.admin.set_delivery_radius_component import (
    set_delivery_radius_component,
)
from app.components.admin.set_opening_hours_component import set_opening_hours_component
from app.components.layout.footer_component import footer_component
from app.components.layout.navbar_component import navbar_component
from app.routes import render_page
from app.models.MenuItem import MenuItem

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


@admin_routes.route("/menu", methods=["GET", "POST"])
def menu_overview() -> Response:
    components = {
        "header": [
            navbar_component(),
        ],
        "aside": [
            aside_menu_component(),
        ],
        "main": [
            menu_page_navigation_component(),
            menu_overview_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("admin.html", "Menu", components)


@admin_routes.route("/menu/add", methods=["GET", "POST"])
def add_menu_item() -> Response:
    components = {
        "header": [
            navbar_component(),
        ],
        "aside": [
            aside_menu_component(),
        ],
        "main": [
            menu_page_navigation_component(),
            add_menu_item_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("admin.html", "Menu - Add Item", components)


@admin_routes.route("/menu/<int:item_id>/edit", methods=["GET", "POST"])
def edit_menu_item(item_id: int) -> Response:
    components = {
        "header": [
            navbar_component(),
        ],
        "aside": [
            aside_menu_component(),
        ],
        "main": [
            menu_page_navigation_component(),
            edit_menu_item_component(item_id),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("admin.html", "Menu - Add Item", components)


@admin_routes.route("/menu/<int:item_id>/delete", methods=["GET"])
def delete_menu_item(item_id: int) -> Response:
    with app.app_context():
        menu_item = MenuItem.query.get_or_404(item_id)

        if menu_item.menu.restaurant != current_user.restaurant:
            abort(403)

        db.session.delete(menu_item)
        db.session.commit()

    flash("Menu item deleted successfully.", "success")

    return redirect(url_for("admin.menu_overview"))


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
            set_delivery_radius_component(),
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
