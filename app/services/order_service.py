from app import db, socketio
from app.components.admin.orders_table_component import orders_table_component
from app.models.Order import Order
from app.enum.OrderStatus import OrderStatus
from app.services.notification_service import push_notification


def update_status(order: Order, new_status_value: str | None) -> None:
    new_status_value = new_status_value.lower().capitalize()

    if new_status_value not in [status.value for status in OrderStatus]:
        push_notification(
            category="danger",
            title="Invalid Status!",
            text="Please choose a valid status.",
            to=order.restaurant.account,
            save_to_db=False,
        )

        return

    order.status = OrderStatus(new_status_value)
    db.session.commit()

    socketio.emit(
        "refresh_orders",
        {"orders": orders_table_component(order.restaurant)},
        to="/restaurant/" + str(order.restaurant.id),
    )

    push_notification(
        category="success",
        title="Order Update!",
        text=f'Order status successfully updated to "{new_status_value}".',
        to=order.restaurant.account,
        save_to_db=False,
    )

    push_notification(
        category="success",
        title="Order Update!",
        text=f"Your order's at ({order.restaurant.name}) status has been updated to {new_status_value}.",
        to=order.customer.account,
    )
