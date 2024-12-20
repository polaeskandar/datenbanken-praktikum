from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

from app.components.layout.navbar_component import navbar_component
from app.components.layout.footer_component import footer_component
from app.routes import render_page
from app.services.component_safe_renderer import safe_render_component

index_routes = Blueprint("index", __name__)


@index_routes.route("/", methods=["GET", "POST"])
@login_required
def index():
    if current_user.is_restaurant():
        return redirect(url_for("admin.index"))

    components = build_components([])

    return render_page("layout.html", "Home", components)


def build_components(main_components: list) -> dict:
    return {
        "header": [safe_render_component(navbar_component)],
        "main": [safe_render_component(c) for c in main_components],
        "footer": [safe_render_component(footer_component)],
    }
