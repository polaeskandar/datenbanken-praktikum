from flask import flash, redirect, request, Response
from werkzeug.exceptions import BadRequest

from app.components.layout.error_component import error_component


def safe_render_component(component_func: callable, *args, **kwargs) -> str | Response:
    try:
        return component_func(*args, **kwargs)
    except BadRequest as e:
        flash(e.description, "danger")

        return redirect(request.referrer)
    except Exception as e:
        raise e
        message = (
            "An error occurred while trying to render this component. "
            "We are alerted and our engineering team is working on it."
        )

        return error_component(message, component_func, e)
