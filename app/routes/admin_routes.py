from flask import Blueprint

from app.components.admin.aside_menu_component import aside_menu_component
from app.components.footer_component import footer_component
from app.components.navbar_component import navbar_component
from app.routes import render_page

admin_routes = Blueprint("admin", __name__)

@admin_routes.route("/")
def index():
    components = {
        "header": [
            navbar_component(),
        ],
        "aside": [
            aside_menu_component(),
        ],
        "main": [],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("admin.html", "Admin", components)