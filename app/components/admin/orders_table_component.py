from flask import render_template
from sqlalchemy import case, asc

from app.components.layout.pagination_component import pagination_component
from app.models.Restaurant import Restaurant
from app.enum.OrderStatus import OrderStatus
from app.models.Order import Order
from app.services.component_service import safe_render_component
from app.services.pagination_service import paginate_query


def orders_table_component(restaurant: Restaurant) -> str:
    paginated_query = paginate_query(
        (
            Order.query.filter_by(restaurant=restaurant).order_by(
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
        "orders": paginated_query.items,
        "pagination_component": safe_render_component(
            lambda: pagination_component(paginated_query)
        ),
        "OrderStatus": OrderStatus,
        "transitions": get_available_transitions(),
    }

    return render_template("components/admin/orders_table.html", attributes=attributes)


def get_available_transitions() -> dict:
    return {
        OrderStatus.PENDING: [OrderStatus.ACCEPTED, OrderStatus.CANCELLED],
        OrderStatus.ACCEPTED: [OrderStatus.COMPLETED, OrderStatus.CANCELLED],
        OrderStatus.COMPLETED: [],
        OrderStatus.CANCELLED: [],
    }
