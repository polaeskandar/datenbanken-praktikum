from flask import render_template

from app.models.Account import Account
from app.models.Notification import Notification


def notifications_component(account: Account | None) -> str | None:
    if account is None:
        return None

    notifications = get_latest_notifications(account)

    attributes = {
        "notifications": notifications,
        "unread_notifications": count_unread_notifications(notifications),
    }

    return render_template(
        "components/layout/notifications.html", attributes=attributes
    )


def count_unread_notifications(notifications: list[Notification]) -> int:
    return sum(1 for notification in notifications if not notification.is_read)


def get_latest_notifications(account: Account | None) -> list:
    if account is None:
        return []

    return (
        Notification.query.filter_by(account=account)
        .order_by(
            Notification.is_read.asc(),
            Notification.created_at.desc(),
        )
        .limit(5)
        .all()
    )
