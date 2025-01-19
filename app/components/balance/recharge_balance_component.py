from flask import render_template

from app.services.balance_service import get_products_map


def recharge_balance_component() -> str:
    attributes = {
        "plans": get_products_map(),
    }

    return render_template(
        "components/balance/recharge_balance.html", attributes=attributes
    )
