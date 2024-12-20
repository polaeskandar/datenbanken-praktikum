from flask import render_template, flash, Response, redirect, url_for
from flask_login import current_user

from app import app, db
from app.form.component.admin.MenuItemForm import MenuItemForm
from app.models.MenuItem import MenuItem
from app.services.upload_image_service import upload_required_file


def add_menu_item_component() -> str | Response:
    menu_item_form = MenuItemForm(item_id=None)

    if menu_item_form.validate_on_submit():
        try:
            return handle_menu_item_creation(menu_item_form)
        except Exception as e:
            flash(f"An error occurred while creating the menu item: {str(e)}", "danger")

    for error in menu_item_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "menu_item_form": menu_item_form,
    }

    return render_template(
        "components/admin/add_menu_item.html",
        attributes=attributes,
    )


def handle_menu_item_creation(menu_item_form: MenuItemForm) -> Response:
    with app.app_context():
        try:
            # Upload image and validate
            image_path = upload_required_file(
                form=menu_item_form,
                err="An image for the item has to be provided.",
            )

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

            raise Exception(f"Failed to create menu item: {str(e)}")

    return redirect(url_for("admin.menu_overview"))
