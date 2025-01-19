from flask import render_template


def search_heading_carousel() -> str:
    return render_template("components/search/search_heading_carousel.html")
