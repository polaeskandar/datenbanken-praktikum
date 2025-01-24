from flask import render_template, url_for

from app.enum.QuerySort import QuerySort
from app.services.restaurant_search_service import RestaurantSearchService


def search_header_component(
    restaurant_search_service: RestaurantSearchService, restaurants_count: int
) -> str:
    terms_list = get_terms_list(restaurant_search_service)

    if len(terms_list) == 0:
        terms_list.append({"label": "All", "link": url_for("index.index")})

    attributes = {
        "terms_list": terms_list,
        "restaurants_count": restaurants_count,
        "QuerySort": QuerySort,
    }

    return render_template(
        "components/search/search_header.html", attributes=attributes
    )


def get_terms_list(restaurant_search_service: RestaurantSearchService):
    restaurant_names_list = (
        restaurant_search_service.get_restaurant_names_as_list() or []
    )

    links = [
        {
            "label": restaurant.capitalize(),
            "link": build_link(restaurant_search_service, restaurant),
        }
        for restaurant in restaurant_names_list
    ]

    return links


def build_link(restaurant_search_service: RestaurantSearchService, without: str) -> str:
    filtered_terms = [
        term.strip().lower()
        for term in (restaurant_search_service.get_restaurant_names_as_list() or [])
        if term.strip().lower() != without.strip().lower()
    ]

    return url_for(
        "index.index",
        search_terms=",".join(filtered_terms),
    )
