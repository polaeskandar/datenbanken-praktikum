from flask import Response, flash, redirect, url_for, request
from flask_login import current_user

from app import db
from app.models.Cart import Cart
from app.models.CartItem import CartItem
from app.models.MenuItem import MenuItem
from app.models.Restaurant import Restaurant


def add_item_to_cart(restaurant: Restaurant, item: MenuItem):
    # Query for the existing Cart
    cart = Cart.query.filter_by(
        customer_id=current_user.customer.id, restaurant_id=restaurant.id
    ).first()

    # Create cart if not found
    if cart is None:
        cart = Cart(customer=current_user.customer, restaurant=restaurant)

        db.session.add(cart)
        db.session.commit()

    # Look up if this item is already in the Cart
    item_in_cart = CartItem.query.filter_by(
        cart_id=cart.id, menu_item_id=item.id
    ).first()

    # If it's not in the cart, create a new CartItem; else increment quantity
    if item_in_cart is None:
        item_in_cart = CartItem(quantity=1, menu_item_id=item.id, cart_id=cart.id)

        db.session.add(item_in_cart)
    else:
        item_in_cart.quantity += 1

    db.session.commit()


def increment_item_quantity_in_cart(
    restaurant: Restaurant, item: MenuItem, cart_id: int
) -> Response:
    cart = Cart.query.filter_by(id=cart_id).first()

    # 1. Check if the cart exists
    if cart is None:
        flash("You don't have any items in your cart yet.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    # 2. Ensure the current user is the owner of this cart
    if current_user.customer.id != cart.customer_id:
        flash("You don't own this cart.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    # 3. Verify the cart belongs to the same restaurant
    if cart.restaurant_id != restaurant.id:
        flash("This cart does not belong to the selected restaurant.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_item_id=item.id).first()

    # 4. Check if the item is in the cart
    if cart_item is None:
        flash("This item is not currently in your cart.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    # 5. Increment the item quantity
    cart_item.quantity += 1

    db.session.commit()
    flash("Item quantity updated.", "success")

    return redirect(request.referrer or url_for("index.index"))


def decrement_item_quantity_in_cart(
    restaurant: Restaurant, item: MenuItem, cart_id: int
) -> Response:
    cart = Cart.query.filter_by(id=cart_id).first()

    # 1. Check if the cart exists
    if cart is None:
        flash("You don't have any items in your cart yet.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    # 2. Ensure the current user is the owner of this cart
    if current_user.customer.id != cart.customer_id:
        flash("You don't own this cart.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    # 3. Verify the cart belongs to the same restaurant
    if cart.restaurant_id != restaurant.id:
        flash("This cart does not belong to the selected restaurant.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_item_id=item.id).first()

    # 4. Check if the item is in the cart
    if cart_item is None:
        flash("This item is not currently in your cart.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    # 5. Increment the item quantity
    cart_item.quantity -= 1

    # 6. If quantity goes to zero or below, remove the item from the cart
    if cart_item.quantity <= 0:
        db.session.delete(cart_item)

    db.session.commit()
    flash("Item quantity updated.", "success")

    return redirect(request.referrer or url_for("index.index"))
