from flask import render_template, Response, redirect, url_for, flash

from app import db
from app.form.profile.RateOrderForm import RateOrderForm
from app.models.Order import Order
from app.services.component_service import flash_errors


def rating_component(order: Order) -> str | Response:
    rate_order_form = RateOrderForm()

    if rate_order_form.validate_on_submit():
        return rate_order(rate_order_form, order)

    flash_errors(rate_order_form)

    attributes = {
        "rate_order_form": rate_order_form,
    }

    return render_template("components/profile/rating.html", attributes=attributes)


def rate_order(rate_order_form: RateOrderForm, order: Order) -> Response:
    rating = rate_order_form.rating.data

    order.rating = rating
    db.session.commit()
    flash("Thanks for leaving your feedback.", "success")

    return redirect(url_for("profile.customer_orders"))
