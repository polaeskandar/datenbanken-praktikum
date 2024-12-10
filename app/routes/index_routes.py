from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user

from app.components.best_bets_component import best_bets_component
from app.components.navbar_component import navbar_component
from app.components.footer_component import footer_component
from app.components.restaurant_card_component import restaurant_card_component
from app.components.restaurant_rating_component import restaurant_rating_component
from app.routes import render_page

index_routes = Blueprint("index", __name__)


@index_routes.route("/", methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    components = {
        "header": [
            navbar_component(),
        ],
        "main": [
            best_bets_component(),
            restaurant_card_component(),
            restaurant_rating_component()
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_page("layout.html", "Home", components)
