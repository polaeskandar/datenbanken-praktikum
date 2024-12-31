from app import socketio, db
from app.components.layout.notifications_component import notifications_component
from app.enum.AccountType import AccountType
from app.models.Account import Account
from app.models.Notification import Notification
from app.services.component_safe_renderer import safe_render_component


def push_notification(
    category: str,
    title: str,
    text: str,
    to: Account,
    save_to_db: bool = True,
) -> None:
    if save_to_db:
        notification = Notification(title=title, text=text, account=to)
        db.session.add(notification)
        db.session.commit()

    room = None

    if to.get_account_type() == AccountType.CUSTOMER:
        room = "/customer/" + str(to.customer.id)
    elif to.get_account_type() == AccountType.RESTAURANT:
        room = "/restaurant/" + str(to.restaurant.id)

    socketio.emit(
        "flash",
        {
            "category": category,
            "title": title,
            "text": text,
            "type": "notification" if save_to_db else "flash",
        },
        to=room,
    )

    socketio.emit(
        "refresh_notifications",
        {
            "notifications": safe_render_component(lambda: notifications_component(to)),
        },
        to=room,
    )
