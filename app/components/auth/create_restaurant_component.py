import os
import string
import random

from flask import render_template, url_for, Response, flash, redirect, request
from flask_login import login_user

from app import app, db
from app.form.component.auth.CreateRestaurantForm import CreateRestaurantForm
from app.models.Account import Account
from app.models.Restaurant import Restaurant
from app.models.PostalCode import PostalCode


def create_restaurant_component():
    create_restaurant_form = CreateRestaurantForm()

    if create_restaurant_form.validate_on_submit():
        return create_restaurant(create_restaurant_form)

    for error in create_restaurant_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "create_restaurant_form": create_restaurant_form,
        "login_route": url_for("auth.login"),
        "register_customer_route": url_for("auth.register"),
    }

    return render_template(
        "components/auth/create_restaurant.html", attributes=attributes
    )


# TODO SOLVE POTENTIAL RACE CONDITION, WHILE CREATING POSTAL CODES
def create_restaurant(register_restaurant_form: CreateRestaurantForm) -> Response:
    with app.app_context():
        postal_code = PostalCode.query.filter_by(
            postal_code=register_restaurant_form.postal_code.data
        ).first()

        if postal_code is None:
            postal_code = PostalCode(
                postal_code=register_restaurant_form.postal_code.data,
            )

            db.session.add(postal_code)

        account = Account(
            email=register_restaurant_form.email.data,
            hashed_password=register_restaurant_form.password.data,
            address=register_restaurant_form.address.data,
            postal_code=postal_code,
        )

        image_path = upload_image(register_restaurant_form)

        restaurant = Restaurant(
            name=register_restaurant_form.name.data,
            description=register_restaurant_form.description.data,
            account=account,
            image=image_path,
        )

        db.session.add(account)
        db.session.add(restaurant)
        db.session.commit()

        login_user(account)
        flash("Restaurant registered successfully!", category="success")

    return redirect(url_for("index.index"))


def upload_image(register_restaurant_form) -> str | None:
    if not register_restaurant_form.image.name in request.files:
        return None

    image = request.files[register_restaurant_form.image.name]

    if image.filename == "":
        return None

    upload_directory = app.config["UPLOAD_DIRECTORY"]

    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    image_path = (
        "".join(random.choices(string.ascii_uppercase + string.digits, k=32))
        + "."
        + image.filename.split(".")[1]
    )

    image.save(os.path.join(app.config["UPLOAD_DIRECTORY"], image_path))

    return image_path
