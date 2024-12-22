from flask import render_template, redirect, url_for

from app.form.component.admin.EditSettingsForm import EditSettingsForm


def edit_settings_component() -> str | Response:
    edit_settings_form = EditSettingsForm()

    if edit_settings_form.validate_on_submit():

        restaurant_name = edit_settings_form.restaurant_name.data
        address = edit_settings_form.address.data
        postal_code = edit_settings_form.postal_code.data
        restaurant_description = edit_settings_form.restaurant_description.data
        image = edit_settings_form.image.data

        filename = None
        if image:
            upload_folder = os.path.join(current_app.root_path, "static/uploads")
            os.makedirs(upload_folder, exist_ok=True)

            if allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(upload_folder, filename))
            else:
                flash("Invalid file format. Please upload a .jpg or .png image.", "danger")
                return render_template(
                    "components/admin/edit_settings.html", attributes={"edit_settings_form": edit_settings_form}
                )

        settings = {
            "restaurant_name": restaurant_name,
            "address": address,
            "postal_code": postal_code,
            "restaurant_description": restaurant_description,
            "image": filename,
        }

        flash("Settings updated successfully!", "success")
        return redirect(url_for("admin.settings"))
        
    attributes = {"edit_settings_form": edit_settings_form}
    return render_template("components/admin/edit_settings.html", attributes=attributes)


def allowed_file(filename):
    """
    Helper function to validate file extensions.
    """
    allowed_extensions = {"jpg", "jpeg", "png"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
