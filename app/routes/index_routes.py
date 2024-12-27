from flask import Blueprint, redirect, url_for, request, Response, flash
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException

from app.components.restaurants.restaurant_menu_component import (
    restaurant_menu_component,
)
from app.models.Restaurant import Restaurant
from app.components.layout.navbar_component import navbar_component
from app.components.layout.footer_component import footer_component
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
from app.services.component_safe_renderer import safe_render_component
from app.services.search.restaurant_search_service import RestaurantSearchService

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


@index_routes.route("/search/<int:restaurant_id>", methods=["GET", "POST"])
def restaurant_page(restaurant_id: int) -> Response:
    try:
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first_or_404(
            restaurant_id
        )
    except HTTPException:
        flash("The requested restaurant does not exist.", "danger")

        return redirect(url_for("index.index"))

    components = build_components_for_restaurant_page(
        [
            lambda: restaurant_header_component(restaurant),
            lambda: restaurant_menu_component(restaurant),
        ],
        [],
    )

    return render_page("restaurant.html", "Home", components)


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
