from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def logout_required(route_function: callable):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in.", "dark")

            return redirect(url_for("index.index"))

        return route_function(*args, **kwargs)

    return decorated_function
