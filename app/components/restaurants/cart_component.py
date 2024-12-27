from decimal import Decimal, ROUND_HALF_UP

from flask import (
    render_template,
    Response,
    flash,
    redirect,
    request,
    url_for,
)
from flask_login import current_user

from app import db
from app.enum.OrderStatus import OrderStatus
from app.form.component.restaurant.PlaceOrderForm import PlaceOrderForm
from app.models.Cart import Cart
from app.models.CartItem import CartItem
from app.models.Order import Order
from app.models.OrderItem import OrderItem
from app.models.Restaurant import Restaurant


def cart_component(restaurant: Restaurant) -> str | Response:
    place_order_form = PlaceOrderForm()
    cart = get_or_create_cart(restaurant)
    cart_items = cart.items if cart.items else []
    total_price = calculate_total_price(cart_items)

    if place_order_form.validate_on_submit():
        return place_order(
            place_order_form=place_order_form,
            restaurant=restaurant,
            total_price=total_price,
            cart=cart,
            cart_items=cart_items,
        )

    for error in place_order_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "restaurant": restaurant,
        "cart": cart,
        "cart_items": cart_items,
        "total_price": f"{total_price:.2f}",
        "place_order_form": place_order_form,
    }

    return render_template("components/restaurants/cart.html", attributes=attributes)


def place_order(
    place_order_form: PlaceOrderForm,
    restaurant: Restaurant,
    total_price: Decimal,
    cart: Cart,
    cart_items: list[CartItem],
) -> Response:
    if not cart_items:
        flash("No items were found in the cart.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    if total_price <= 0:
        flash("Cannot charge a non-positive value.", "danger")

        return redirect(request.referrer or url_for("index.index"))

    try:
        wishes_text = place_order_form.wishes_text.data

        order = Order(
            status=OrderStatus.PENDING,
            price=float(total_price),
            customer=current_user.customer,
            restaurant=restaurant,
            wishes_text=wishes_text,
        )

        # Create OrderItems for each CartItem, capturing quantity
        for cart_item in cart_items:
            order_item = OrderItem(
                order=order, item=cart_item.item, quantity=cart_item.quantity
            )

            db.session.add(order_item)

        db.session.delete(cart)
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

        raise e

    flash(
        "The order has been successfully placed. The restaurant will be notified shortly.",
        "success",
    )

    return redirect(url_for("index.index"))


def get_or_create_cart(restaurant: Restaurant) -> Cart:
    cart = Cart.query.filter_by(
        restaurant_id=restaurant.id, customer_id=current_user.customer.id
    ).first()

    if cart is None:
        cart = Cart(restaurant_id=restaurant.id, customer_id=current_user.customer.id)
        db.session.add(cart)
        db.session.commit()

    return cart


def calculate_total_price(cart_items: list[CartItem]) -> Decimal:
    """
    Sums up the price * quantity for each cart item using precise Decimal arithmetic.
    """

    total = Decimal("0.00")

    for cart_item in cart_items:
        # Convert the float to a string before Decimal to minimize float precision issues
        price = Decimal(str(cart_item.item.price))
        quantity = Decimal(str(cart_item.quantity))
        total += price * quantity

    # Round to two decimal places using a standard rounding mode
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
