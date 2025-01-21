from flask import render_template
from flask_sqlalchemy.pagination import Pagination

from app.components.layout.pagination_component import pagination_component
from app.services.component_service import safe_render_component


def restaurants_list_component(restaurants: Pagination) -> str:
    attributes = {
        "restaurants": restaurants,
        "pagination_component": safe_render_component(
            lambda: pagination_component(restaurants)
        ),
    }

    return render_template(
        "components/search/restaurants_list_component.html", attributes=attributes
    )
