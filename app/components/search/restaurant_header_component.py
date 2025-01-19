from flask import render_template, url_for

from app.models.Restaurant import Restaurant


def restaurant_header_component(restaurant: Restaurant) -> str:
    attributes = {
        "results_url": url_for("index.index"),
        "restaurant": restaurant,
    }

    return render_template(
        "components/search/restaurant_header.html",
        attributes=attributes,
    )
