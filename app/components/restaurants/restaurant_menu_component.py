from flask import render_template

from app.models.Restaurant import Restaurant


def restaurant_menu_component(restaurant: Restaurant):
    return render_template("components/restaurants/restaurant_menu.html")
