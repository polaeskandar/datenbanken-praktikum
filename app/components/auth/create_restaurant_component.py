from flask import render_template, url_for, Response, flash, redirect
from flask_login import login_user

from app import app, db
from app.form.component.auth.CreateRestaurantForm import CreateRestaurantForm
from app.models.Account import Account
from app.models.Restaurant import Restaurant
from app.models.PostalCode import PostalCode
from app.models.Menu import Menu
from app.services.postal_code_service import get_or_create_postal_code
from app.services.upload_image_service import upload_file


def create_restaurant_component() -> str | Response:
    create_restaurant_form = CreateRestaurantForm()

    if create_restaurant_form.validate_on_submit():
        return handle_restaurant_creation(create_restaurant_form)

    for error in create_restaurant_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "create_restaurant_form": create_restaurant_form,
        "login_route": url_for("auth.login"),
        "register_customer_route": url_for("auth.register"),
    }

    return render_template(
        "components/auth/create_restaurant.html",
        attributes=attributes,
    )


def handle_restaurant_creation(
    create_restaurant_form: CreateRestaurantForm,
) -> Response:
    with app.app_context():
        try:
            # Ensure the postal code exists or create it
            postal_code = get_or_create_postal_code(
                create_restaurant_form.postal_code.data
            )

            # Create the account
            account = create_account(create_restaurant_form, postal_code)

            # Handle optional image upload
            image_path = upload_file(create_restaurant_form)

            # Create the restaurant
            restaurant = Restaurant(
                name=create_restaurant_form.name.data,
                description=create_restaurant_form.description.data,
                account=account,
                image=image_path,
            )

            # Create the associated menu
            menu = Menu(restaurant=restaurant)

            # Save all entities to the database
            db.session.add_all([account, restaurant, menu])
            db.session.commit()

            # Log the user in and redirect
            login_user(account)
            flash("Restaurant registered successfully!", category="success")

            return redirect(url_for("admin.index"))
        except Exception as e:
            db.session.rollback()

            raise e


def create_account(form: CreateRestaurantForm, postal_code: PostalCode) -> Account:
    return Account(
        email=form.email.data,
        hashed_password=form.password.data,
        address=form.address.data,
        postal_code=postal_code,
    )
