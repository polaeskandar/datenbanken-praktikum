from flask import render_template


def recharge_balance_failure_component() -> str:
    return render_template("components/balance/recharge_balance_failure.html")
