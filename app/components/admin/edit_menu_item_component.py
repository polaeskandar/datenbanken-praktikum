import os
import string
import random

from flask import render_template, abort, request, Response, flash, redirect, url_for
from flask_login import current_user

from app import app, db
from app.form.component.admin.MenuItemForm import MenuItemForm
from app.models.MenuItem import MenuItem


def edit_menu_item_component(item_id: int) -> str | Response:
    menu_item = MenuItem.query.get_or_404(item_id)

    if menu_item.menu.restaurant != current_user.restaurant:
        abort(403)

    menu_item_form = MenuItemForm(
        item_name=menu_item.name,
        price=menu_item.price,
        description=menu_item.description,
    )

    menu_item_form.item_id = menu_item.id

    if menu_item_form.validate_on_submit():
        return update_item(menu_item_form, menu_item)

    for error in menu_item_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "menu_item_form": menu_item_form,
        "item_name": menu_item.name,
    }

    return render_template(
        "components/admin/edit_menu_item.html", attributes=attributes
    )


def update_item(menu_item_form: MenuItemForm, menu_item: MenuItem) -> Response:
    with app.app_context():
        # Ensure the menu_item is attached to the current session
        menu_item = db.session.merge(menu_item)

        menu_item.name = menu_item_form.item_name.data
        menu_item.price = menu_item_form.price.data
        menu_item.description = menu_item_form.description.data

        image_path = upload_image(menu_item_form)
        if image_path is not None:
            menu_item.image = image_path

        db.session.commit()

        flash("Updated menu item successfully.", "success")

        return redirect(url_for("admin.menu_overview"))


def upload_image(menu_item_form: MenuItemForm) -> str | None:
    if not menu_item_form.image.name in request.files:
        return None

    image = request.files[menu_item_form.image.name]

    if image.filename == "":
        return None

    upload_directory = app.config["UPLOAD_DIRECTORY"]

    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    image_path = (
        "".join(random.choices(string.ascii_uppercase + string.digits, k=32))
        + "."
        + image.filename.split(".")[1]
    )

    image.save(os.path.join(app.config["UPLOAD_DIRECTORY"], image_path))

    return image_path
