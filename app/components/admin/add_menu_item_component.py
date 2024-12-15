import os
import string
import random

from flask import render_template, flash, Response, request, redirect, url_for
from flask_login import current_user

from app import app, db
from app.form.component.admin.MenuItemForm import MenuItemForm
from app.models.MenuItem import MenuItem


def add_menu_item_component() -> str | Response:
    menu_item_form = MenuItemForm()

    if menu_item_form.validate_on_submit():
        return create_menu_item(menu_item_form)

    for error in menu_item_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "menu_item_form": menu_item_form,
    }

    return render_template("components/admin/add_menu_item.html", attributes=attributes)


def create_menu_item(menu_item_form) -> Response:
    with app.app_context():
        try:
            image_path = upload_image(menu_item_form)
        except Exception as e:
            flash(str(e), category="danger")

            return redirect(url_for("admin.add_menu_item"))

        menu_item = MenuItem(
            name=menu_item_form.item_name.data,
            description=menu_item_form.description.data,
            price=menu_item_form.price.data,
            image=image_path,
            menu=current_user.restaurant.menu,
        )

        db.session.add(menu_item)
        db.session.commit()

    flash("Item created successfully", category="success")

    return redirect(url_for("admin.menu_overview"))


def upload_image(menu_item_form) -> str:
    if not menu_item_form.image.name in request.files:
        raise Exception("Image for an Item should be uploaded.")

    image = request.files[menu_item_form.image.name]

    if image.filename == "":
        raise Exception("Image for an Item should be uploaded.")

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
