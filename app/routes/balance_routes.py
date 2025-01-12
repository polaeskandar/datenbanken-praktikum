from flask import Blueprint, Response, request

from app.components.customer.recharge_balance_component import (
    recharge_balance_component,
)
from app.components.customer.recharge_balance_failure_component import (
    recharge_balance_failure_component,
)
from app.enum.Layout import Layout
from app.services.balance_service import start_checkout_session, fill_balance
from app.services.component_safe_renderer import render_page, build_components

balance_routes = Blueprint("balance", __name__)


@balance_routes.route("/recharge", methods=["GET"])
def balance_recharge() -> Response:
    components = build_components(main_components=[recharge_balance_component])

    return render_page(Layout.DEFAULT, "Recharge Account's Balance", components)


@balance_routes.route("/checkout/<string:product_id>", methods=["GET"])
def checkout(product_id: str) -> Response:
    return start_checkout_session(product_id)


@balance_routes.route("/checkout/success", methods=["GET"])
def checkout_success() -> Response:
    session_id = request.args.get("session_id")

    return fill_balance(session_id)


@balance_routes.route("/checkout/failure", methods=["GET"])
def checkout_failure() -> Response:
    components = build_components(main_components=[recharge_balance_failure_component])

    return render_page(Layout.DEFAULT, "Failed Payment", components)
