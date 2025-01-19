from flask import Blueprint, Response, flash, redirect, url_for, request
from werkzeug.exceptions import HTTPException

from app.models import Restaurant, MenuItem
from app.services.cart_service import (
    add_item_to_cart,
    increment_item_quantity_in_cart,
    decrement_item_quantity_in_cart,
)

cart_routes = Blueprint("cart", __name__)


@cart_routes.route(
    "/search/<int:restaurant_id>/cart/add/<int:item_id>", methods=["GET"]
)
def add_to_cart(restaurant_id: int, item_id: int) -> Response:
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        item = MenuItem.query.get_or_404(item_id)
    except HTTPException:
        flash("The requested restaurant or item does not exist.", "danger")

        return redirect(url_for("index.index"))

    add_item_to_cart(restaurant=restaurant, item=item)

    flash("Item added to cart.", "success")

    return redirect(request.referrer or url_for("index.index"))


@cart_routes.route(
    "/search/<int:restaurant_id>/cart/<int:cart_id>/increment/<int:item_id>",
    methods=["GET"],
)
def increment_item_quantity(restaurant_id: int, cart_id: int, item_id: int) -> Response:
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        item = MenuItem.query.get_or_404(item_id)
    except HTTPException:
        flash("The requested restaurant or item does not exist.", "danger")

        return redirect(url_for("index.index"))

    return increment_item_quantity_in_cart(
        restaurant=restaurant, item=item, cart_id=cart_id
    )


@cart_routes.route(
    "/search/<int:restaurant_id>/cart/<int:cart_id>/decrement/<int:item_id>",
    methods=["GET"],
)
def decrement_item_quantity(restaurant_id: int, cart_id: int, item_id: int) -> Response:
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        item = MenuItem.query.get_or_404(item_id)
    except HTTPException:
        flash("The requested restaurant or item does not exist.", "danger")

        return redirect(url_for("index.index"))

    return decrement_item_quantity_in_cart(
        restaurant=restaurant, item=item, cart_id=cart_id
    )
