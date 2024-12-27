from flask import render_template

from app.models.Restaurant import Restaurant


def restaurant_menu_component(restaurant: Restaurant):
    menu_items = restaurant.menu.items.all()

    attributes = {"restaurant": restaurant, "menu_items": menu_items}

    return render_template(
        "components/restaurants/restaurant_menu.html", attributes=attributes
    )
