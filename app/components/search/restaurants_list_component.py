from flask import render_template

from app.models.Restaurant import Restaurant


def restaurants_list_component(restaurants: list[Restaurant]) -> str:
    attributes = {
        "restaurants": restaurants,
    }

    return render_template(
        "components/search/restaurants_list_component.html", attributes=attributes
    )
