from flask import render_template


def footer_component() -> str:
    return render_template("components/layout/footer.html")
