import os

from flask import render_template, redirect, url_for, flash, Response
from flask_login import current_user
from werkzeug.utils import secure_filename

from app import db
from app.form.component.admin.EditSettingsForm import EditSettingsForm
from app.models.Restaurant import Restaurant
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
        current_user.restaurant.name = edit_settings_form.restaurant_name.data
        current_user.address = edit_settings_form.address.data
        current_user.postal_code = get_or_create_postal_code(
            edit_settings_form.postal_code.data
        )
        current_user.restaurant.description = (
            edit_settings_form.restaurant_description.data
        )
        current_user.restaurant.image = upload_file(edit_settings_form)

        db.session.commit()
        flash("Settings updated successfully!", "success")

        return redirect(url_for("admin.settings"))

    for error in edit_settings_form.errors.values():
        flash(error[0], category="danger")

    attributes = {"edit_settings_form": edit_settings_form}

    return render_template("components/admin/edit_settings.html", attributes=attributes)
