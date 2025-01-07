from flask import render_template
from flask_login import current_user
from sqlalchemy import case, asc

from app.enum.OrderStatus import OrderStatus
from app.models.Order import Order


def customer_order_component():
    orders = (
        Order.query.filter_by(customer_id=current_user.customer.id)
        .order_by(
            case(
                (Order.status == OrderStatus.PENDING, 0),
                (Order.status == OrderStatus.ACCEPTED, 1),
                (Order.status == OrderStatus.COMPLETED, 2),
                (Order.status == OrderStatus.CANCELLED, 3),
                else_=9999,
            ),
            asc(Order.ordered_at),
        )
        .all()
    )

    attributes = {
        "orders": orders,
        "OrderStatus": OrderStatus,
    }

    return render_template(
        "components/profile/customer_order.html", attributes=attributes
    )
