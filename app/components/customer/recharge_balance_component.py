from flask import Response, render_template

from app.services.balance_service import get_products_map


def recharge_balance_component() -> str | Response:

    attributes = {
        "plans": get_products_map(),
    }

    return render_template(
        "components/customer/recharge_balance.html", attributes=attributes
    )
