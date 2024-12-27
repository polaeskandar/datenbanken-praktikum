from flask import abort, flash
from flask_login import current_user

from app import app, db

from app.models.MenuItem import MenuItem


def delete_item(item_id: int):
    menu_item = MenuItem.query.get_or_404(item_id)

    if menu_item.menu.restaurant != current_user.restaurant:
        abort(403)

    db.session.delete(menu_item)
    db.session.commit()

    flash("Menu item deleted successfully.", "success")
