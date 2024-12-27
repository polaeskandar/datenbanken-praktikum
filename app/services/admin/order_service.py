from flask import request, flash, redirect, url_for

from app import db
from app.models.Order import Order
from app.enum.OrderStatus import OrderStatus


def update_status(order: Order):
    new_status_value = request.form.get("status").lower().capitalize()

    if not new_status_value:
        flash("No status selected.", "danger")

        return redirect(url_for("admin.index"))

    if new_status_value not in [status.value for status in OrderStatus]:
        flash("Invalid status.", "danger")

        return redirect(url_for("admin.index"))

    order.status = OrderStatus(new_status_value)

    db.session.commit()
    flash(f'Order status updated to "{new_status_value}".', "success")

    return redirect(url_for("admin.index"))
