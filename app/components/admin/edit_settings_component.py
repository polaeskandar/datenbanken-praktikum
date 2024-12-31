from flask import render_template, redirect, url_for, flash, current_app, Response
from werkzeug.utils import secure_filename
from app.form.component.admin.EditSettingsForm import EditSettingsForm
import os


def edit_settings_component() -> str | Response:
    edit_settings_form = EditSettingsForm()

    if edit_settings_form.validate_on_submit():

        restaurant_details = get_restaurant_details(edit_settings_form)

        image = edit_settings_form.image.data
        filename = upload_file(edit_settings_form)

        if not filename and image:
            flash("Invalid file format. Please upload a .jpg or .png image.", "danger")
            return render_template(
                "components/admin/edit_settings.html", attributes={"edit_settings_form": edit_settings_form}
            )

        settings = {
            **restaurant_details,
            "image": filename,
        }

        flash("Settings updated successfully!", "success")
        return redirect(url_for("admin.settings"))

    attributes = {"edit_settings_form": edit_settings_form}
    return render_template("components/admin/edit_settings.html", attributes=attributes)


def upload_file(form: EditSettingsForm, upload_directory: str = None) -> str | None:

    try:
        image = form.image.data
        if not image:
            return None

        upload_folder = upload_directory or os.path.join(current_app.root_path, "static/uploads")
        os.makedirs(upload_folder, exist_ok=True)

        if allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(upload_folder, filename))
            return filename
        return None

    except BadRequest:
        return None


def get_restaurant_details(form: EditSettingsForm) -> dict:

    return {
        "restaurant_name": form.restaurant_name.data,
        "address": form.address.data,
        "postal_code": form.postal_code.data,
        "restaurant_description": form.restaurant_description.data,
    }
