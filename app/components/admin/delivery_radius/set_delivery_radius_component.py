from flask import Flask, render_template, url_for, redirect, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from app import db
from app.models.Restaurant import Restaurant
from app.models.PostalCode import PostalCode
from app.models.PostalCodeRestaurant import PostalCodeRestaurant
from app.form.component.admin.SetDeliveryRadiusForm import SetDeliveryRadiusForm


def set_delivery_radius_component():
    postal_codes = PostalCode.query.all()
    postal_code_choices = [(postal.id, postal.postal_code) for postal in postal_codes]

    set_delivery_radius_form = SetDeliveryRadiusForm()
    set_delivery_radius_form.postal_code.choices = postal_code_choices

    if set_delivery_radius_form.validate_on_submit():
        return set_postal_code_restaurant(set_delivery_radius_form)

    attributes = {"set_delivery_radius_form": set_delivery_radius_form}

    return render_template(
        "components/admin/set_delivery_radius.html", attributes=attributes
    )


def set_postal_code_restaurant(
    set_delivery_radius_form: SetDeliveryRadiusForm,
) -> Response:
    postal_code_id = set_delivery_radius_form.postal_code.data
    distance = set_delivery_radius_form.distance.data

    postal_code_restaurant = PostalCodeRestaurant.query.filter_by(
        restaurant_id=current_user.restaurant.id, postal_code_id=postal_code_id
    ).first()

    if postal_code_restaurant:
        postal_code_restaurant.distance = distance
    else:
        postal_code_restaurant = PostalCodeRestaurant(
            restaurant_id=current_user.restaurant.id,
            postal_code_id=postal_code_id,
            distance=distance,
        )

        db.session.add(postal_code_restaurant)

    flash("Delivery radius set successfully!", "success")
    db.session.commit()

    return redirect(url_for("admin.delivery_radius"))
