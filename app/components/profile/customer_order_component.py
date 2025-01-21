from flask import render_template
from flask_login import current_user
from sqlalchemy import case, asc

from app.components.layout.pagination_component import pagination_component
from app.enum.OrderStatus import OrderStatus
from app.models.Order import Order
from app.services.component_service import safe_render_component
from app.services.pagination_service import paginate_query


def customer_order_component() -> str:
    orders = paginate_query(
        (
            Order.query.filter_by(customer_id=current_user.customer.id).order_by(
                case(
                    (Order.status == OrderStatus.PENDING, 0),
                    (Order.status == OrderStatus.ACCEPTED, 1),
                    (Order.status == OrderStatus.COMPLETED, 2),
                    (Order.status == OrderStatus.CANCELLED, 3),
                    else_=9999,
                ),
                asc(Order.ordered_at),
            )
        )
    )

    attributes = {
        "orders": orders,
        "pagination_component": safe_render_component(
            lambda: pagination_component(orders)
        ),
        "OrderStatus": OrderStatus,
    }

    return render_template(
        "components/profile/customer_order.html", attributes=attributes
    )
