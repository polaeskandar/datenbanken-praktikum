from flask import Blueprint, Response

from app.components.customer.customer_order_component import customer_order_component
from app.enum.Layout import Layout
from app.services.component_safe_renderer import render_page, build_components

profile_routes = Blueprint("profile", __name__)


@profile_routes.route("/orders")
def customer_orders() -> Response:
    components = build_components(
        main_components=[
            customer_order_component,
        ]
    )

    return render_page(Layout.DEFAULT, "Recharge Account's Balance", components)
