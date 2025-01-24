from flask import Blueprint, Response, abort
from flask_login import current_user

from app.components.profile.customer_order_component import customer_order_component
from app.components.profile.rating_component import rating_component
from app.enum.Layout import Layout
from app.models.Order import Order
from app.services.component_service import render_page, build_components

profile_routes = Blueprint("profile", __name__)


@profile_routes.route("/orders", methods=["GET"])
def customer_orders() -> Response:
    components = build_components(
        main_components=[
            customer_order_component,
        ]
    )

    return render_page(Layout.DEFAULT, "Recharge Account's Balance", components)


@profile_routes.route("/orders/<int:order_id>/rating", methods=["GET", "POST"])
def rate_order(order_id: int) -> Response:
    order = Order.query.get_or_404(order_id)

    if order.customer != current_user.customer:
        abort(403)

    components = build_components(
        main_components=[
            lambda: rating_component(order),
        ]
    )

    return render_page(Layout.DEFAULT, "Leave Rating", components)
