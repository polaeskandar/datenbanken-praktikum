from flask import render_template, flash, redirect, url_for, Response
from flask_login import login_user

from app import app, db
from app.form.component.auth.RegisterCustomerForm import RegisterCustomerForm
from app.models.Account import Account
from app.models.Customer import Customer
from app.models.PostalCode import PostalCode


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


# TODO SOLVE POTENTIAL RACE CONDITION, WHILE CREATING POSTAL CODES
def create_customer(register_customer_form: RegisterCustomerForm) -> Response:
    with app.app_context():
        postal_code = PostalCode.query.filter_by(
            postal_code=register_customer_form.postal_code.data
        ).first()

        if postal_code is None:
            postal_code = PostalCode(
                postal_code=register_customer_form.postal_code.data,
            )

            db.session.add(postal_code)

        account = Account(
            email=register_customer_form.email.data,
            hashed_password=register_customer_form.password.data,
            address=register_customer_form.address.data,
            postal_code=postal_code,
        )

        customer = Customer(
            first_name=register_customer_form.first_name.data,
            last_name=register_customer_form.last_name.data,
            account=account,
        )

        db.session.add(account)
        db.session.add(customer)
        db.session.commit()

        login_user(account)
        flash("User created successfully!", category="success")

    return redirect(url_for("index.index"))
