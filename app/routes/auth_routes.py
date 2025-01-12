from flask import Blueprint, Response, redirect, url_for, flash
from flask_login import logout_user, login_required

from app.components.auth.create_restaurant_component import create_restaurant_component
from app.components.auth.login_component import login_component
from app.components.auth.register_customer_component import register_customer_component
from app.enum.Layout import Layout
from app.middleware.logout_required import logout_required
from app.services.component_safe_renderer import (
    render_page,
    build_components,
)

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    components = build_components(main_components=[register_customer_component])

    return render_page(Layout.DEFAULT, "Register", components)


@auth_routes.route("/", methods=["GET", "POST"])
@auth_routes.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    components = build_components(main_components=[login_component])

    return render_page(Layout.DEFAULT, "Login", components)


@auth_routes.route("/become-a-partner", methods=["GET", "POST"])
@logout_required
def register_restaurant():
    components = build_components(main_components=[create_restaurant_component])

    return render_page(Layout.DEFAULT, "Become a Partner", components)


@auth_routes.route("/logout", methods=["GET"])
@login_required
def logout() -> Response:
    logout_user()
    flash("You have been logged out.", "dark")

    return redirect(url_for("auth.login"))
