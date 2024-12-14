from flask import render_template, redirect, url_for

from app.form.component.admin.EditSettingsForm import EditSettingsForm


def edit_settings_component():
    edit_settings_form = EditSettingsForm()

    if edit_settings_form.validate_on_submit():
        return redirect(url_for("admin.settings"))

    attributes = {
        "edit_settings_form": edit_settings_form,
    }

    return render_template("components/admin/edit_settings.html", attributes=attributes)
