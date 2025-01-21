from flask import render_template
from flask_sqlalchemy.pagination import Pagination


def pagination_component(pagination: Pagination):
    attributes = {"pagination": pagination}

    return render_template("components/layout/pagination.html", attributes=attributes)
