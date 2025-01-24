from flask import request
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query


def paginate_query(query: Query) -> Pagination:
    return query.paginate(page=request.args.get("page", 1, type=int), per_page=5)
