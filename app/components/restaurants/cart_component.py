from flask import render_template
from flask_login import current_user

from app import db
from app.models.Cart import Cart
from app.models.Restaurant import Restaurant


def cart_component(restaurant: Restaurant):
    cart = get_or_create_cart(restaurant)
    cart_items = cart.items if cart.items else []
    total_price = calculate_total_price(cart_items)

    attributes = {
        "restaurant": restaurant,
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price,
    }

    return render_template("components/restaurants/cart.html", attributes=attributes)


def get_or_create_cart(restaurant: Restaurant) -> Cart:
    cart = Cart.query.filter_by(
        restaurant_id=restaurant.id, customer_id=current_user.customer.id
    ).first()

    if cart is None:
        cart = Cart(restaurant_id=restaurant.id, customer_id=current_user.customer.id)

        db.session.add(cart)
        db.session.commit()

    return cart


def calculate_total_price(cart_items) -> float:
    return round(sum(item.item.price * item.quantity for item in cart_items), 2)
