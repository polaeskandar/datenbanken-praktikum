from flask import render_template, request

from app.dto.RestaurantSearchContext import RestaurantSearchContext
from app.services.search.restaurant_search_service import RestaurantSearchService


def restaurants_list_component():
    restaurant_search_context = RestaurantSearchContext(
        restaurant_names=request.args.get("search_term"),
        postal_codes=request.args.get("postal_code"),
    )

    restaurant_search_service = RestaurantSearchService(restaurant_search_context)
    restaurants = restaurant_search_service.fetch_restaurants()

    attributes = {
        "restaurants": restaurants,
    }

    return render_template(
        "components/search/restaurants_list_component.html", attributes=attributes
    )
