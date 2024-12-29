from flask import render_template
from sqlalchemy import case

from app.models.Restaurant import Restaurant
from app.enum.OrderStatus import OrderStatus
from app.models.Order import Order


def orders_table_component(restaurant: Restaurant) -> str:
    orders = (
        Order.query.filter_by(restaurant=restaurant)
        .order_by(
            case(
                (Order.status == OrderStatus.PENDING, 0),
                (Order.status == OrderStatus.COMPLETED, 1),
                (Order.status == OrderStatus.CANCELLED, 2),
                else_=3,
            )
        )
        .all()
    )

    attributes = {"orders": orders, "OrderStatus": OrderStatus}

    return render_template("components/admin/orders_table.html", attributes=attributes)
