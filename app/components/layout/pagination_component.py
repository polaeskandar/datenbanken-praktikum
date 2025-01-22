from flask import render_template
from flask_sqlalchemy.pagination import Pagination


def pagination_component(pagination: Pagination) -> str:
    if pagination.total == 0:
        return ""

    attributes = {"pagination": pagination}

    return render_template("components/layout/pagination.html", attributes=attributes)
