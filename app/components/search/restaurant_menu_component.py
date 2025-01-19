from flask import render_template

from app.models.Restaurant import Restaurant


def restaurant_menu_component(restaurant: Restaurant) -> str:
    menu_items = restaurant.menu.items.all()

    attributes = {"restaurant": restaurant, "menu_items": menu_items}

    return render_template(
        "components/search/restaurant_menu.html",
        attributes=attributes,
    )
