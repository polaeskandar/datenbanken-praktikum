from flask import render_template, url_for, redirect, flash, Response
from flask_login import current_user

from app import db
from app.form.admin.SetDeliveryRadiusForm import SetDeliveryRadiusForm
from app.models.PostalCodeRestaurant import PostalCodeRestaurant
from app.services.component_service import flash_errors
from app.services.postal_code_service import get_or_create_postal_code


def set_delivery_radius_component() -> str | Response:
    set_delivery_radius_form = SetDeliveryRadiusForm()

    if set_delivery_radius_form.validate_on_submit():
        return set_postal_code_restaurant(set_delivery_radius_form)

    flash_errors(set_delivery_radius_form)

    attributes = {"set_delivery_radius_form": set_delivery_radius_form}

    return render_template(
        "components/admin/delivery_radius/set_delivery_radius.html",
        attributes=attributes,
    )


def set_postal_code_restaurant(
    set_delivery_radius_form: SetDeliveryRadiusForm,
) -> Response:
    postal_code = get_or_create_postal_code(set_delivery_radius_form.postal_code.data)
    distance = set_delivery_radius_form.distance.data

    postal_code_restaurant = PostalCodeRestaurant.query.filter_by(
        restaurant_id=current_user.restaurant.id, postal_code_id=postal_code.id
    ).first()

    if postal_code_restaurant:
        postal_code_restaurant.distance = distance
    else:
        postal_code_restaurant = PostalCodeRestaurant(
            restaurant_id=current_user.restaurant.id,
            postal_code_id=postal_code.id,
            distance=distance,
        )

        db.session.add(postal_code_restaurant)

    flash("Delivery radius set successfully!", "success")
    db.session.commit()

    return redirect(url_for("admin.delivery_radius"))
