from flask import render_template, flash, Response, redirect, url_for
from flask_login import current_user

from app import db
from app.form.admin.MenuItemForm import MenuItemForm
from app.models.MenuItem import MenuItem
from app.services.component_service import flash_errors
from app.services.upload_image_service import upload_file


def add_menu_item_component() -> str | Response:
    menu_item_form = MenuItemForm(item_id=None)

    if menu_item_form.validate_on_submit():
        return handle_menu_item_creation(menu_item_form)

    flash_errors(menu_item_form)

    attributes = {
        "menu_item_form": menu_item_form,
    }

    return render_template(
        "components/admin/menu/add_menu_item.html",
        attributes=attributes,
    )


def handle_menu_item_creation(menu_item_form: MenuItemForm) -> Response:
    try:
        # Upload image and validate
        image_path = upload_file(form=menu_item_form)

        # Create and save the menu item
        menu_item = MenuItem(
            name=menu_item_form.item_name.data,
            description=menu_item_form.description.data,
            price=menu_item_form.price.data,
            image=image_path,
            menu=current_user.restaurant.menu,
        )

        db.session.add(menu_item)
        db.session.commit()

        flash("Item created successfully.", "success")
    except Exception as e:
        db.session.rollback()

        raise e

    return redirect(url_for("admin.menu_overview"))
