from flask import render_template


def get_delivery_radius_component() -> str:
    return render_template("components/admin/get_delivery_radius.html")
