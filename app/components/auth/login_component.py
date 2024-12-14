from flask import render_template, Response, redirect, url_for, flash
from flask_login import login_user

from app.models.Account import Account
from app.form.component.auth.LoginForm import LoginForm


def login_component() -> Response | str:
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return login(login_form)

    for error in login_form.errors.values():
        flash(error[0], category="danger")

    attributes = {
        "login_form": login_form,
        "register_route": url_for("auth.register"),
        "register_restaurant_route": url_for("auth.register_restaurant"),
    }

    return render_template(
        "components/auth/login.html",
        attributes=attributes,
    )


def login(login_form) -> Response:
    account = Account.query.filter_by(email=login_form.email.data).first()

    if account.verify_password(login_form.password.data):
        login_user(account)
        flash(f"Welcome back! {login_form.email.data}", category="success")

        return redirect(url_for("index.index"))

    flash("Invalid email or password.", category="danger")

    return redirect(url_for("auth.login"))