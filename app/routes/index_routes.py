from flask import Blueprint, redirect, url_for, request, Response, flash, abort
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException

from app import db
from app.components.customer.recharge_balance_component import (
    recharge_balance_component,
)
from app.components.restaurants.restaurant_menu_component import (
    restaurant_menu_component,
)
from app.models.Cart import Cart
from app.models.CartItem import CartItem
from app.models.Restaurant import Restaurant
from app.models.MenuItem import MenuItem
from app.components.layout.navbar_component import navbar_component
from app.components.layout.footer_component import footer_component
from app.components.restaurants.cart_component import cart_component
from app.components.restaurants.restaurant_header_component import (
    restaurant_header_component,
)
from app.components.search.restaurants_list_component import restaurants_list_component
from app.components.search.search_header_component import search_header_component
from app.components.search.search_heading_carousel_component import (
    search_heading_carousel,
)
from app.dto.RestaurantSearchContext import RestaurantSearchContext
from app.routes import render_page
from app.services.balance_service import start_checkout_session, fill_balance
from app.services.component_safe_renderer import safe_render_component
from app.services.search.restaurant_search_service import RestaurantSearchService
from app.services.restaurant.cart_service import (
    add_item_to_cart,
    increment_item_quantity_in_cart,
    decrement_item_quantity_in_cart,
)

index_routes = Blueprint("index", __name__)


@index_routes.route("/", methods=["GET", "POST"])
@index_routes.route("/search", methods=["GET", "POST"])
@login_required
def index() -> Response:
    if current_user.is_restaurant():
        return redirect(url_for("admin.index"))

    restaurant_search_context = RestaurantSearchContext(
        restaurant_names=request.args.get("search_terms"),
        postal_codes=request.args.get("postal_codes"),
    )

    restaurant_search_service = RestaurantSearchService(restaurant_search_context)
    restaurants = restaurant_search_service.fetch_restaurants()

    components = build_components(
        [
            lambda: search_header_component(
                restaurant_search_service, len(restaurants)
            ),
            search_heading_carousel,
            lambda: restaurants_list_component(restaurants),
        ]
    )

    return render_page("layout.html", "Home", components)


@index_routes.route("/balance/recharge", methods=["GET"])
def balance_recharge() -> Response:
    components = build_components(
        [
            recharge_balance_component,
        ]
    )

    return render_page("layout.html", "Recharge Account's Balance", components)


@index_routes.route("/balance/checkout/<string:product_id>", methods=["GET"])
def checkout(product_id: str) -> Response:
    return start_checkout_session(product_id)


@index_routes.route("/balance/checkout/success", methods=["GET"])
def checkout_success() -> Response:
    session_id = request.args.get("session_id")

    return fill_balance(session_id)


@index_routes.route("/balance/checkout/failure", methods=["GET"])
def checkout_failure() -> Response:
    raise Exception(request)


@index_routes.route("/search/<int:restaurant_id>", methods=["GET", "POST"])
def restaurant_page(restaurant_id: int) -> Response:
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
    except HTTPException:
        flash("The requested restaurant does not exist.", "danger")

        return redirect(url_for("index.index"))

    components = build_components_for_restaurant_page(
        [
            lambda: restaurant_header_component(restaurant),
            lambda: restaurant_menu_component(restaurant),
        ],
        [
            lambda: cart_component(restaurant),
        ],
    )

    return render_page("restaurant.html", "Home", components)


@index_routes.route(
    "/search/<int:restaurant_id>/cart/add/<int:item_id>", methods=["GET"]
)
def add_to_cart(restaurant_id: int, item_id: int) -> Response:
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        item = MenuItem.query.get_or_404(item_id)
    except HTTPException:
        flash("The requested restaurant or item does not exist.", "danger")

        return redirect(url_for("index.index"))

    add_item_to_cart(restaurant=restaurant, item=item)

    flash("Item added to cart.", "success")

    return redirect(request.referrer or url_for("index.index"))


@index_routes.route(
    "/search/<int:restaurant_id>/cart/<int:cart_id>/increment/<int:item_id>",
    methods=["GET"],
)
def increment_item_quantity(restaurant_id: int, cart_id: int, item_id: int) -> Response:
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        item = MenuItem.query.get_or_404(item_id)
    except HTTPException:
        flash("The requested restaurant or item does not exist.", "danger")

        return redirect(url_for("index.index"))

    return increment_item_quantity_in_cart(
        restaurant=restaurant, item=item, cart_id=cart_id
    )


@index_routes.route(
    "/search/<int:restaurant_id>/cart/<int:cart_id>/decrement/<int:item_id>",
    methods=["GET"],
)
def decrement_item_quantity(restaurant_id: int, cart_id: int, item_id: int) -> Response:
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        item = MenuItem.query.get_or_404(item_id)
    except HTTPException:
        flash("The requested restaurant or item does not exist.", "danger")

        return redirect(url_for("index.index"))

    return decrement_item_quantity_in_cart(
        restaurant=restaurant, item=item, cart_id=cart_id
    )


def build_components(main_components: list) -> dict:
    return {
        "header": [safe_render_component(navbar_component)],
        "main": [safe_render_component(c) for c in main_components],
        "footer": [safe_render_component(footer_component)],
    }


def build_components_for_restaurant_page(
    main_components: list, aside_components: list
) -> dict:
    return {
        "header": [safe_render_component(navbar_component)],
        "main": [safe_render_component(mc) for mc in main_components],
        "aside": [safe_render_component(ac) for ac in aside_components],
        "footer": [safe_render_component(footer_component)],
    }
