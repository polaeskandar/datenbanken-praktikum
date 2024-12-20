from flask import render_template
from app import app


def error_component(message: str, component_func: callable, err: Exception) -> str:
    if app.debug:
        message += f" Component: {component_func.__name__}. Error: {err}"

    attributes = {
        "message": message,
    }

    return render_template(
        "components/layout/error.html",
        attributes=attributes,
    )
