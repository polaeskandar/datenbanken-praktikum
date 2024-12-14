from flask import render_template


def get_delivery_radius_component():
    return render_template("components/admin/get_delivery_radius.html")