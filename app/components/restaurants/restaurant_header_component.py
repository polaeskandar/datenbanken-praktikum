from flask import render_template, request, url_for

from app.models.Restaurant import Restaurant


def restaurant_header_component(restaurant: Restaurant):
    attributes = {
        "results_url": get_results_url(),
        "restaurant_name": restaurant.name,
    }

    return render_template(
        "components/restaurants/restaurant_header.html",
        attributes=attributes,
    )


def get_results_url() -> str:
    url = request.referrer

    if url is None:
        return url_for("index.index")

    return url
