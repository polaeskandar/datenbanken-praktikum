from flask import render_template, flash, redirect, url_for, Response
from flask_login import login_user

from app import app, db
from app.form.component.auth.RegisterCustomerForm import RegisterCustomerForm
from app.models.Account import Account
from app.models.Customer import Customer
from app.models.PostalCode import PostalCode
from app.services.postal_code_service import get_or_create_postal_code


def register_customer_component() -> Response | str:
    register_customer_form = RegisterCustomerForm()

    if register_customer_form.validate_on_submit():
        return handle_customer_creation(register_customer_form)

    for error in register_customer_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "register_customer_form": register_customer_form,
        "login_route": url_for("auth.login"),
        "register_restaurant_route": url_for("auth.register_restaurant"),
    }

    return render_template(
        "components/auth/register_customer.html",
        attributes=attributes,
    )


def handle_customer_creation(register_customer_form: RegisterCustomerForm) -> Response:
    with app.app_context():
        try:
            # Ensure the postal code exists or create it
            postal_code = get_or_create_postal_code(
                register_customer_form.postal_code.data
            )

            # Create the account
            account = create_account(register_customer_form, postal_code)

            # Create the customer
            customer = create_customer_entity(register_customer_form, account)

            # Save all entities to the database
            db.session.add_all([account, customer])
            db.session.commit()

            # Log the user in and redirect
            login_user(account)
            flash("User created successfully!", category="success")

            return redirect(url_for("index.index"))
        except Exception as e:
            db.session.rollback()

            raise e


def create_account(form: RegisterCustomerForm, postal_code: PostalCode) -> Account:
    return Account(
        email=form.email.data,
        hashed_password=form.password.data,
        address=form.address.data,
        postal_code=postal_code,
    )


def create_customer_entity(form: RegisterCustomerForm, account: Account) -> Customer:
    return Customer(
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        account=account,
    )
