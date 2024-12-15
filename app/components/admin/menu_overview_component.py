from flask import render_template
from flask_login import current_user

from app.models.MenuItem import MenuItem


def menu_overview_component():
    menu_id = current_user.restaurant.menu.id
    menu_items = MenuItem.query.filter_by(menu_id=menu_id).all()

    attributes = {
        "menu_items": menu_items,
    }

    return render_template(
        "components/admin/menu_overview_component.html", attributes=attributes
    )
