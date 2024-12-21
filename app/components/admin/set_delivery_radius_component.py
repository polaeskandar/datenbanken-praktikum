from flask import render_template, url_for, redirect, Response

from app.form.component.admin.SetDeliveryRadiusForm import SetDeliveryRadiusForm
from app.models.PostalCode import PostalCode


def set_delivery_radius_component() -> str | Response:
    postal_codes = PostalCode.query.all()
    choices = [(str(postal.id), postal.postal_code) for postal in postal_codes]

    set_delivery_radius_form = SetDeliveryRadiusForm()
    set_delivery_radius_form.postal_code.choices += choices

    if set_delivery_radius_form.validate_on_submit():
        # TODO Implement
        return redirect(url_for("admin.delivery_radius"))

    attributes = {"set_delivery_radius_form": set_delivery_radius_form}

    return render_template(
        "components/admin/set_delivery_radius.html", attributes=attributes
    )
