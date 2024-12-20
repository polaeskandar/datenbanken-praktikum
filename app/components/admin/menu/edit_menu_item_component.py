from flask import render_template, abort, Response, flash, redirect, url_for
from flask_login import current_user

from app import app, db
from app.form.component.admin.MenuItemForm import MenuItemForm
from app.models.MenuItem import MenuItem
from app.services.upload_image_service import upload_file


def edit_menu_item_component(item_id: int) -> str | Response:
    # Fetch the menu item or return a 404 if it doesn't exist
    menu_item = MenuItem.query.get_or_404(item_id)

    # Ensure the current user is authorized to edit the menu item
    if not is_user_authorized(menu_item):
        abort(403, description="You do not have permission to edit this menu item.")

    # Pre-fill the form with the existing menu item data
    menu_item_form = MenuItemForm(
        item_id=item_id,
        item_name=menu_item.name,
        price=menu_item.price,
        description=menu_item.description,
    )

    if menu_item_form.validate_on_submit():
        try:
            return handle_menu_item_update(menu_item_form, menu_item)
        except Exception as e:
            flash(f"An error occurred while updating the item: {str(e)}", "danger")

    for error in menu_item_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "menu_item_form": menu_item_form,
        "item_name": menu_item.name,
    }

    return render_template(
        "components/admin/edit_menu_item.html",
        attributes=attributes,
    )


def handle_menu_item_update(
    menu_item_form: MenuItemForm, menu_item: MenuItem
) -> Response:
    with app.app_context():
        try:
            # Update menu item fields
            menu_item.name = menu_item_form.item_name.data
            menu_item.price = menu_item_form.price.data
            menu_item.description = menu_item_form.description.data

            # Handle optional image upload
            image_path = upload_file(menu_item_form)
            if image_path:
                menu_item.image = image_path

            # Commit changes to the database
            db.session.commit()
            flash("Updated menu item successfully.", "success")
        except Exception as e:
            db.session.rollback()

            raise Exception(f"Failed to update menu item: {str(e)}")

    return redirect(url_for("admin.menu_overview"))


def is_user_authorized(menu_item: MenuItem) -> bool:
    return (
        hasattr(menu_item.menu, "restaurant")
        and menu_item.menu.restaurant == current_user.restaurant
    )
