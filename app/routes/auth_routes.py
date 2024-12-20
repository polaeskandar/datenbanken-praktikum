from flask import Blueprint, Response, redirect, url_for, flash
from flask_login import logout_user

from app.components.auth.create_restaurant_component import create_restaurant_component
from app.components.auth.login_component import login_component
from app.components.auth.register_customer_component import register_customer_component
from app.components.layout.footer_component import footer_component
from app.components.layout.navbar_component import navbar_component
from app.routes import render_page

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    components = {
        "header": [
            navbar_component(),
        ],
        "main": [
            register_customer_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("layout.html", "Register", components)


@auth_routes.route("/", methods=["GET", "POST"])
@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    components = {
        "header": [
            navbar_component(),
        ],
        "main": [login_component()],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("layout.html", "Login", components)


@auth_routes.route("/become-a-partner", methods=["GET", "POST"])
def register_restaurant():
    components = {
        "header": [
            navbar_component(),
        ],
        "main": [
            create_restaurant_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("layout.html", "Become a Partner", components)


@auth_routes.route("/logout", methods=["GET"])
def logout() -> Response:
    logout_user()
    flash("You have been logged out.", "dark")

    return redirect(url_for("index.index"))
