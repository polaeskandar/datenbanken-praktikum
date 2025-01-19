from flask import render_template, redirect, url_for, flash, Response
from flask_login import current_user

from app import db
from app.form.admin.EditSettingsForm import EditSettingsForm
from app.services.component_service import flash_errors
from app.services.postal_code_service import get_or_create_postal_code
from app.services.upload_image_service import upload_file


def edit_settings_component() -> str | Response:
    edit_settings_form = EditSettingsForm(
        restaurant_name=current_user.restaurant.name,
        address=current_user.address,
        postal_code=current_user.postal_code.postal_code,
        restaurant_description=current_user.restaurant.description,
    )

    if edit_settings_form.validate_on_submit():
        return update_restaurant_details(edit_settings_form)

    flash_errors(edit_settings_form)

    attributes = {"edit_settings_form": edit_settings_form}

    return render_template("components/admin/edit_settings.html", attributes=attributes)


def update_restaurant_details(edit_settings_form) -> Response:
    current_user.restaurant.name = edit_settings_form.restaurant_name.data
    current_user.address = edit_settings_form.address.data
    current_user.postal_code = get_or_create_postal_code(
        edit_settings_form.postal_code.data
    )
    current_user.restaurant.description = edit_settings_form.restaurant_description.data

    # Handle optional image upload
    image_path = upload_file(edit_settings_form)
    if image_path:
        current_user.restaurant.image = image_path

    db.session.commit()
    flash("Settings updated successfully!", "success")

    return redirect(url_for("admin.settings"))
