from flask import render_template
from flask_login import current_user

from app import app, db
from app.models.Cart import Cart
from app.models.Restaurant import Restaurant

def cart_component(restaurant: Restaurant):
    cart = Cart.query.filter_by(
        restaurant_id=restaurant.id,
        customer_id=current_user.customer.id
    ).first()

    if cart is None:
        cart = Cart(
            restaurant_id=restaurant.id,
            customer_id=current_user.customer.id
        )

        cart_items = []

        db.session.add(cart)
        db.session.commit()
        
    else:
        cart_items = cart.items

    total_price = sum(item.item.price * item.quantity for item in cart_items)

    attributes = {
        "restaurant": restaurant,
        "cart": cart,
        "cart_items": cart_items,
        "total_price": f"{total_price:.2f}",
    }

    return render_template("components/restaurants/cart.html", attributes=attributes)