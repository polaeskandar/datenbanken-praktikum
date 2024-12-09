from flask import render_template, Blueprint

from app.components.navbar_component import navbar_component
from app.components.footer_component import footer_component
from app.components.restaurant_card_component import restaurant_card_component
from app.components.best_bets_component import best_bets_component
from app.components.restaurant_rating_component import restaurant_rating_component
from app.components.head_pic_itemauswahl_component import head_pic_itemauswahl_component

routes_blueprint = Blueprint("routes", __name__)


@routes_blueprint.route("/", methods=["GET", "POST"])
def index():
    components = {
        "header": [
            navbar_component(),
        ],
        "main": [
            best_bets_component(),
            restaurant_card_component(),
            restaurant_rating_component(),
            head_pic_itemauswahl_component(),
        ],
        "footer": [
            footer_component(),
        ],
    }

    return render_template(
        "layout.html",
        components=components,
        page_title="Home",
    )
