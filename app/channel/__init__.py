from flask_socketio import join_room
from werkzeug.exceptions import HTTPException

from app import socketio, db
from app.models.Notification import Notification
from app.models.Customer import Customer
from app.models.Order import Order
from app.services.order_service import update_status
from app.services.notification_service import push_notification


@socketio.on("join")
def on_join(data) -> None:
    room = data["room"]
    join_room(room)
    print(f"User joined room: {room}")


@socketio.on("order_status_changed")
def order_status_changed(data: dict[str, str]) -> None:
    order_id = data.get("orderId")
    new_status = data.get("newStatus")
    room = data.get("room")

    try:
        order = Order.query.get_or_404(order_id)
    except HTTPException as e:
        push_notification(
            category="danger",
            title="Something went wrong!",
            text="Order is not found.",
            to=Customer.query.get(room).account,
            save_to_db=False,
        )

        return

    update_status(order, new_status)


@socketio.on("read_notifications")
def read_notifications(data) -> None:
    notification_ids = data.get("notificationIds")

    notifications = Notification.query.filter(
        Notification.id.in_(notification_ids)
    ).all()

    for notification in notifications:
        notification.is_read = True

    db.session.commit()
