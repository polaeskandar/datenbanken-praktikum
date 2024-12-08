from flask import Blueprint, Response, redirect, url_for
from flask_login import logout_user

from app.components.auth.register_customer_component import register_customer_component
from app.routes import render_page

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/register", methods=["GET", "POST"])
def register_customer_view():
    components = {
        "header": [],
        "main": [
            register_customer_component(),
        ],
        "footer": [],
    }

    return render_page("layout.html", "Register", components)


@auth_routes.route("/", methods=["GET", "POST"])
@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    components = {
        "header": [],
        "main": [],
        "footer": [],
    }

    return render_page("layout.html", "Login", components)


@auth_routes.route("/become-a-partner", methods=["GET", "POST"])
def register_restaurant():
    components = {
        "header": [],
        "main": [],
        "footer": [],
    }

    return render_page("layout.html", "Become a Partner", components)


@auth_routes.route("/logout", methods=["GET"])
def logout() -> Response:
    logout_user()

    return redirect(url_for("index.index"))
