from flask import render_template, url_for, request, flash
from flask_wtf import FlaskForm

from app.form.component.navbar.RestaurantsFilterForm import RestaurantsFilterForm


def navbar_component():
    restaurants_filter_form = RestaurantsFilterForm(request.args)

    if not restaurants_filter_form.validate():
        for error in restaurants_filter_form.errors.values():
            flash(error[0], category="danger")

    attributes = {
        "logo": url_for("static", filename="images/logo.png"),
        "index_route": url_for("routes.index"),
        "restaurants_filter_form": restaurants_filter_form,
    }

    return render_template("components/navbar.html", attributes=attributes)
