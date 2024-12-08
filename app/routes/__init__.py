from flask import Response, render_template


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


from app.routes import index_routes
from app.routes import auth_routes
