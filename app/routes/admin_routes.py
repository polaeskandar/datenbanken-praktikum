from flask import Blueprint, Response, abort, flash, redirect, url_for, request
from flask_login import login_required

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
from app.services.admin.menu_service import delete_item
from app.services.component_safe_renderer import safe_render_component

admin_routes = Blueprint("admin", __name__)


@admin_routes.route("/")
@admin_routes.route("/orders")
@login_required
def index() -> Response:
    components = build_components([orders_table_component])

    return render_page("admin.html", "Admin", components)


@admin_routes.route("/menu", methods=["GET", "POST"])
@login_required
def menu_overview() -> Response:
    components = build_components(
        [menu_page_navigation_component, menu_overview_component]
    )

    return render_page("admin.html", "Menu", components)


@admin_routes.route("/menu/add", methods=["GET", "POST"])
@login_required
def add_menu_item() -> Response:
    components = build_components(
        [menu_page_navigation_component, add_menu_item_component]
    )

    return render_page("admin.html", "Menu - Add Item", components)


@admin_routes.route("/menu/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_menu_item(item_id: int) -> Response:
    components = build_components(
        [menu_page_navigation_component, lambda: edit_menu_item_component(item_id)]
    )

    return render_page("admin.html", "Menu - Edit Item", components)


@admin_routes.route("/menu/<int:item_id>/delete", methods=["GET"])
@login_required
def delete_menu_item(item_id: int) -> Response:
    delete_item(item_id)

    return redirect(url_for("admin.menu_overview"))


@admin_routes.route("/opening-hours", methods=["GET", "POST"])
@login_required
def opening_hours() -> Response:
    components = build_components([set_opening_hours_component])

    return render_page("admin.html", "Opening Hours", components)


@admin_routes.route("/delivery_radius", methods=["GET", "POST"])
@login_required
def delivery_radius() -> Response:
    components = build_components(
        [set_delivery_radius_component, get_delivery_radius_component]
    )

    return render_page("admin.html", "Delivery Radius", components)


@admin_routes.route("/settings", methods=["GET", "POST"])
@login_required
def settings() -> Response:
    components = build_components([edit_settings_component])

    return render_page("admin.html", "Settings", components)


def build_components(main_components: list) -> dict:
    return {
        "header": [safe_render_component(navbar_component)],
        "aside": [safe_render_component(aside_menu_component)],
        "main": [safe_render_component(mc) for mc in main_components],
        "footer": [safe_render_component(footer_component)],
    }
