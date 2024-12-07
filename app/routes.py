from flask import render_template, Blueprint, Response, redirect, url_for
from flask_login import logout_user

from app.components.navbar_component import navbar_component
from app.components.footer_component import footer_component
from app.components.auth.register_customer_component import register_customer_component

routes_blueprint = Blueprint("routes", __name__)


@routes_blueprint.route("/", methods=["GET", "POST"])
def index():
    components = {
        "header": [
            navbar_component(),
        ],
        "main": [],
        "footer": [
            footer_component(),
        ],
    }

    return render_template(
        "layout.html",
        components=components,
        page_title="Home",
    )


@routes_blueprint.route("/auth/register", methods=["GET", "POST"])
def register_customer_view():
    components = {
        "header": [],
        "main": [
            register_customer_component(),
        ],
        "footer": [],
    }

    for section, section_components in components.items():
        for component_item in section_components:
            if type(component_item) is Response:
                return component_item

    return render_template(
        "layout.html",
        components=components,
        page_title="Register",
    )


@routes_blueprint.route("/auth", methods=["GET", "POST"])
@routes_blueprint.route("/auth/login", methods=["GET", "POST"])
def login():
    components = {
        "header": [],
        "main": [],
        "footer": [],
    }

    return render_template(
        "layout.html",
        components=components,
        page_title="Login",
    )


@routes_blueprint.route("/auth/become-a-partner", methods=["GET", "POST"])
def register_restaurant():
    components = {
        "header": [],
        "main": [],
        "footer": [],
    }

    return render_template(
        "layout.html",
        components=components,
        page_title="Become a Partner",
    )


@routes_blueprint.route("/auth/logout", methods=["GET"])
def logout() -> Response:
    logout_user()

    return redirect(url_for("routes.index"))
