from flask import render_template, Response, redirect, url_for, flash
from flask_login import login_user

from app.enum.AccountType import AccountType
from app.models.Account import Account
from app.form.auth.LoginForm import LoginForm
from app.services.component_service import flash_errors


def login_component() -> Response | str:
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return handle_login(login_form)

    flash_errors(login_form)

    attributes = {
        "login_form": login_form,
        "register_route": url_for("auth.register"),
        "register_restaurant_route": url_for("auth.register_restaurant"),
    }

    return render_template(
        "components/auth/login.html",
        attributes=attributes,
    )


def handle_login(login_form: LoginForm) -> Response:
    account = Account.query.filter_by(email=login_form.email.data).first()

    # Check if account exists, not of type "PLATFORM" and the password is also correct
    if (
        account
        and account.verify_password(login_form.password.data)
        and account.type != AccountType.PLATFORM
    ):
        login_user(account)
        flash(f"Welcome back, {account.email}!", category="success")

        return redirect(url_for("index.index"))

    # Incase the account is of type "PLATFORM"
    if (
        account
        and account.verify_password(login_form.password.data)
        and account.type == AccountType.PLATFORM
    ):
        flash(f"Unable to login into Platform account.", category="warning")

        return redirect(url_for("index.index"))

    # Invalid credentials
    flash("Invalid email or password.", category="danger")

    return redirect(url_for("auth.login"))
