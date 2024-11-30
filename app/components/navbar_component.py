from flask import render_template, url_for


def navbar_component():
    attributes = {
        "logo": url_for("static", filename="images/logo.png"),
        "index_route": url_for("routes.index"),
    }

    return render_template("components/navbar.html", attributes=attributes)
