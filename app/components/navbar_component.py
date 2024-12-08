from flask import render_template, url_for, request, flash
from flask_login import current_user

from app.enum.AccountType import AccountType
from app.form.component.navbar.RestaurantsFilterForm import RestaurantsFilterForm


def navbar_component() -> str:
    restaurants_filter_form = RestaurantsFilterForm(request.args)

    validate_form(restaurants_filter_form)

    attributes = {
        "logo": url_for("static", filename="images/logo.png"),
        "index_route": url_for("index.index"),
        "login_route": url_for("auth.login"),
        "restaurants_filter_form": restaurants_filter_form,
        "dropdown_label": get_dropdown_label(),
        "dropdown_items": get_dropdown_items(),
    }

    return render_template("components/navbar.html", attributes=attributes)


def validate_form(restaurants_filter_form) -> None:
    if not restaurants_filter_form.validate():
        for error in restaurants_filter_form.errors.values():
            flash(error[0], category="danger")


def get_dropdown_label() -> str | None:
    if current_user.is_anonymous:
        return None

    if current_user.get_account_type() == AccountType.CUSTOMER:
        return f"Hi, {current_user.customer.first_name}!"

    if current_user.get_account_type() == AccountType.RESTAURANT:
        return current_user.restaurant.name

    raise Exception("Invalid account type.")


def get_dropdown_items() -> list[dict[str:str]]:
    if current_user.is_anonymous:
        return []

    if current_user.get_account_type() == AccountType.CUSTOMER:
        return [
            {
                "icon": "fa-solid fa-user me-2",
                "link": url_for("index.index"),
                "text": "View Profile",
            },
            {
                "icon": "fa-solid fa-right-from-bracket me-2",
                "link": url_for("auth.logout"),
                "text": "Logout",
            },
        ]

    if current_user.get_account_type() == AccountType.RESTAURANT:
        return []
