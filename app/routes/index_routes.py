from flask import Blueprint, redirect, url_for, request, Response, flash
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException

from app.components.search.restaurant_menu_component import (
    restaurant_menu_component,
)
from app.enum.Layout import Layout
from app.models.Restaurant import Restaurant
from app.components.cart.cart_component import cart_component
from app.components.search.restaurant_header_component import (
    restaurant_header_component,
)
from app.components.search.restaurants_list_component import restaurants_list_component
from app.components.search.search_header_component import search_header_component
from app.components.search.search_heading_carousel_component import (
    search_heading_carousel,
)
from app.dto.RestaurantSearchContext import RestaurantSearchContext
from app.services.component_service import render_page, build_components
from app.services.restaurant_search_service import RestaurantSearchService

index_routes = Blueprint("index", __name__)


@index_routes.route("/", methods=["GET", "POST"])
@index_routes.route("/search", methods=["GET", "POST"])
@login_required
def index() -> Response:
    if current_user.is_restaurant():
        return redirect(url_for("admin.index"))

    restaurant_search_context = RestaurantSearchContext(
        restaurant_names=request.args.get("search_terms"),
    )

    restaurant_search_service = RestaurantSearchService(restaurant_search_context)
    restaurants = restaurant_search_service.fetch_restaurants()

    components = build_components(
        main_components=[
            lambda: search_header_component(
                restaurant_search_service, len(restaurants)
            ),
            search_heading_carousel,
            lambda: restaurants_list_component(restaurants),
        ],
    )

    return render_page(Layout.DEFAULT, "Home", components)


@index_routes.route("/search/<int:restaurant_id>", methods=["GET", "POST"])
def restaurant_page(restaurant_id: int) -> Response:
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
    except HTTPException:
        flash("The requested restaurant does not exist.", "danger")

        return redirect(url_for("index.index"))

    components = build_components(
        main_components=[
            lambda: restaurant_header_component(restaurant),
            lambda: restaurant_menu_component(restaurant),
        ],
        aside_components=[
            lambda: cart_component(restaurant),
        ],
    )

    return render_page(Layout.RESTAURANT, "Home", components)
