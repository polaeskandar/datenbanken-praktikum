from os import getenv

import stripe
from flask import Response, flash, redirect, request, url_for
from flask_login import current_user
from werkzeug.exceptions import BadRequest

from app import db
from app.enum.AccountType import AccountType
from app.models.Account import Account
from app.models.Order import Order

cached_products = {}


def init_stripe() -> None:
    stripe.api_key = getenv("STRIPE_SECRET_KEY")


def start_checkout_session(product_id: str) -> Response:
    product_key = get_product_key(product_id)

    if not product_key:
        flash("Product not found.", "danger")

        return redirect(request.referrer)

    product = stripe.Product.retrieve(product_key)
    price = product.default_price

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=f"{request.url_root}balance/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{request.url_root}balance/checkout/failure?session_id={{CHECKOUT_SESSION_ID}}",
    )

    return redirect(checkout_session.url, code=303)


def fill_balance(session_id: str) -> Response:
    items = stripe.checkout.Session.retrieve(
        session_id, expand=["line_items.data"]
    ).line_items.data

    for item in items:
        amount_total = item.amount_total
        current_user.balance += amount_total / 100

    db.session.commit()
    flash("Balance has been successfully filled!", "success")

    return redirect(url_for("index.index"))


def charge_balance(order: Order) -> None:
    if current_user.balance - order.price <= 0:
        raise BadRequest("Not enough money to place your order!")

    order.customer.account.balance -= order.price
    order.restaurant.account.balance += round(order.price * (85 / 100), 2)

    platform = Account.query.filter_by(type=AccountType.PLATFORM).first()

    if platform is None:
        raise BadRequest("Platform account not found.")

    platform.balance += round(order.price * (15 / 100), 2)


def get_products_map() -> dict:
    global cached_products

    if not cached_products:
        cached_products = stripe.Product.list(active=True)

    processed_products = {}

    for product in cached_products.data:
        processed_products[product.id] = {**product.metadata}

    return processed_products


def get_product_key(key):
    for k, v in get_products_map().items():
        if k == key:
            return key

    return None
