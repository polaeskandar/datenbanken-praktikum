from functools import wraps
from flask import redirect, url_for, flash, Response, render_template
from flask_login import current_user


def render_page(
    template: str,
    page_title: str,
    components: dict[str, list[str | Response]],
) -> str | Response:
    for section, section_components in components.items():
        for component_item in section_components:
            if type(component_item) is Response:
                return component_item

    return render_template(
        template,
        components=components,
        page_title=page_title,
    )


def logout_required(route_function: callable):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in.", "dark")

            return redirect(url_for("index.index"))

        return route_function(*args, **kwargs)

    return decorated_function


from app.routes import index_routes
from app.routes import auth_routes
from app.routes import admin_routes
