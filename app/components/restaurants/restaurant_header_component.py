from flask import render_template, request, url_for

from app.models.Restaurant import Restaurant


def restaurant_header_component(restaurant: Restaurant):
    attributes = {
        "results_url": url_for("index.index"),
        "restaurant": restaurant,
    }

    return render_template(
        "components/restaurants/restaurant_header.html",
        attributes=attributes,
    )
