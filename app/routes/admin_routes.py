from flask import Blueprint, Response, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app import db
from app.components.admin.menu.add_menu_item_component import add_menu_item_component
from app.components.admin.menu.edit_menu_item_component import edit_menu_item_component
from app.components.admin.edit_settings_component import edit_settings_component
from app.components.admin.delivery_radius.get_delivery_radius_component import (
    get_delivery_radius_component,
)
from app.components.admin.menu.menu_overview_component import menu_overview_component
from app.components.admin.menu.menu_page_navigation_component import (
    menu_page_navigation_component,
)
from app.components.admin.orders_table_component import orders_table_component
from app.components.admin.delivery_radius.set_delivery_radius_component import (
    set_delivery_radius_component,
)
from app.components.admin.set_opening_hours_component import set_opening_hours_component
from app.enum.Layout import Layout
from app.models.PostalCodeRestaurant import PostalCodeRestaurant
from app.services.menu_service import delete_item
from app.services.aside_component_service import get_aside_component_for_admin_board
from app.services.component_service import render_page, build_components

admin_routes = Blueprint("admin", __name__)


@admin_routes.route("/")
@admin_routes.route("/orders")
@login_required
def index() -> Response:
    components = build_components(
        main_components=[lambda: orders_table_component(current_user.restaurant)],
        aside_components=[get_aside_component_for_admin_board],
    )

    return render_page(Layout.SPLIT, "Admin", components)


@admin_routes.route("/menu", methods=["GET", "POST"])
@login_required
def menu_overview() -> Response:
    components = build_components(
        main_components=[menu_page_navigation_component, menu_overview_component],
        aside_components=[get_aside_component_for_admin_board],
    )

    return render_page(Layout.SPLIT, "Menu", components)


@admin_routes.route("/menu/add", methods=["GET", "POST"])
@login_required
def add_menu_item() -> Response:
    components = build_components(
        main_components=[menu_page_navigation_component, add_menu_item_component],
        aside_components=[get_aside_component_for_admin_board],
    )

    return render_page(Layout.SPLIT, "Menu - Add Item", components)


@admin_routes.route("/menu/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_menu_item(item_id: int) -> Response:
    components = build_components(
        main_components=[
            menu_page_navigation_component,
            lambda: edit_menu_item_component(item_id),
        ],
        aside_components=[get_aside_component_for_admin_board],
    )

    return render_page(Layout.SPLIT, "Menu - Edit Item", components)


@admin_routes.route("/menu/<int:item_id>/delete", methods=["GET"])
@login_required
def delete_menu_item(item_id: int) -> Response:
    delete_item(item_id)

    return redirect(url_for("admin.menu_overview"))


@admin_routes.route("/opening-hours", methods=["GET", "POST"])
@login_required
def opening_hours() -> Response:
    components = build_components(
        main_components=[set_opening_hours_component],
        aside_components=[get_aside_component_for_admin_board],
    )

    return render_page(Layout.SPLIT, "Opening Hours", components)


@admin_routes.route("/delivery_radius", methods=["GET", "POST"])
@login_required
def delivery_radius() -> Response:
    components = build_components(
        main_components=[set_delivery_radius_component, get_delivery_radius_component],
        aside_components=[get_aside_component_for_admin_board],
    )

    return render_page(Layout.SPLIT, "Delivery Radius", components)


@admin_routes.route(
    "/delivery_radius/<int:postal_code_restaurant_id>/delete", methods=["GET"]
)
@login_required
def delete_delivery_radius(postal_code_restaurant_id: int) -> Response:
    postal_code = PostalCodeRestaurant.query.get_or_404(postal_code_restaurant_id)

    if postal_code.restaurant != current_user.restaurant:
        abort(403)

    db.session.delete(postal_code)
    db.session.commit()

    flash("Postal code removed successfully.", "success")

    return redirect(url_for("admin.delivery_radius"))


@admin_routes.route("/settings", methods=["GET", "POST"])
@login_required
def settings() -> Response:
    components = build_components(
        main_components=[edit_settings_component],
        aside_components=[get_aside_component_for_admin_board],
    )

    return render_page(Layout.SPLIT, "Settings", components)
