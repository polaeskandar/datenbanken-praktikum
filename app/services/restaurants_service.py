from flask import flash
from flask_login import current_user


def display_warning() -> None:
    if not current_user.restaurant.is_available():
        flash(
            """
            Your restaurant is marked as closed in the current restaurants list.
            Make sure you set the opening hours correctly and have at least one item
            in your menu.
        """,
            "warning",
        )
