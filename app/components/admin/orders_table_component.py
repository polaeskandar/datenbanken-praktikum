from flask import render_template


def orders_table_component() -> str:
    return render_template("components/admin/orders_table.html")
