from flask import render_template, flash, redirect, url_for, Response
from flask_login import login_user

from app import app, db
from app.form.component.auth.RegisterCustomerForm import RegisterCustomerForm
from app.models.Account import Account
from app.models.Customer import Customer


def register_customer_component() -> Response | str:
    register_customer_form = RegisterCustomerForm()

    if register_customer_form.validate_on_submit():
        return create_customer(register_customer_form)

    for error in register_customer_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "register_customer_form": register_customer_form,
    }

    return render_template(
        "components/auth/register_customer.html",
        attributes=attributes,
    )


def create_customer(register_customer_form: RegisterCustomerForm) -> Response:
    account = Account(
        email=register_customer_form.email.data,
        hashed_password=register_customer_form.password.data,
    )

    customer = Customer(
        first_name=register_customer_form.first_name.data,
        last_name=register_customer_form.last_name.data,
        account=account,
    )

    with app.app_context():
        db.session.add(account)
        db.session.add(customer)
        db.session.commit()
        login_user(account)

    flash(
        "User created successfully!", category="success"
    )

    return redirect(url_for("index.index"))
