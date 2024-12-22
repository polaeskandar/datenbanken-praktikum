from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

from app.components.layout.navbar_component import navbar_component
from app.components.layout.footer_component import footer_component
from app.components.search.restaurants_list_component import restaurants_list_component
from app.components.search.search_header_component import search_header_component
from app.components.search.search_heading_carousel import search_heading_carousel
from app.routes import render_page
from app.services.component_safe_renderer import safe_render_component

index_routes = Blueprint("index", __name__)


@index_routes.route("/", methods=["GET", "POST"])
@index_routes.route("/search", methods=["GET", "POST"])
@login_required
def index():
    if current_user.is_restaurant():
        return redirect(url_for("admin.index"))

    components = build_components(
        [
            search_header_component,
            search_heading_carousel,
            restaurants_list_component,
        ]
    )

    return render_page("layout.html", "Home", components)


def build_components(main_components: list) -> dict:
    return {
        "header": [safe_render_component(navbar_component)],
        "main": [safe_render_component(c) for c in main_components],
        "footer": [safe_render_component(footer_component)],
    }
