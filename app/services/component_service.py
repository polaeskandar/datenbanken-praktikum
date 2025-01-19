from flask import redirect, flash, Response, render_template, request
from flask_wtf import FlaskForm

from werkzeug.exceptions import BadRequest

from app.components.layout.error_component import error_component
from app.components.layout.footer_component import footer_component
from app.components.layout.navbar_component import navbar_component
from app.enum.Layout import Layout


def flash_errors(form: FlaskForm) -> None:
    for error in form.errors.values():
        flash(error[0], category="danger")


def build_components(
    main_components: list,
    aside_components: list | None = None,
) -> dict:
    if aside_components is None:
        aside_components = []

    return {
        "header": [safe_render_component(navbar_component)],
        "main": [safe_render_component(mc) for mc in main_components],
        "aside": [safe_render_component(ac) for ac in aside_components],
        "footer": [safe_render_component(footer_component)],
    }


def safe_render_component(component_func: callable, *args, **kwargs) -> str | Response:
    try:
        return component_func(*args, **kwargs)
    except BadRequest as e:
        flash(e.description, "danger")

        return redirect(request.referrer)
    except Exception as e:
        message = (
            "An error occurred while trying to render this component. "
            "We are alerted and our engineering team is working on it."
        )

        return error_component(message, component_func, e)


def render_page(
    template: Layout,
    page_title: str,
    components: dict[str, list[str | Response]],
) -> str | Response:
    for section, section_components in components.items():
        for component_item in section_components:
            if type(component_item) is Response:
                return component_item

    return render_template(
        template.value,
        components=components,
        page_title=page_title,
    )
