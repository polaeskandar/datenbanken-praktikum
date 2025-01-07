from flask import render_template


def aside_menu_component(links: list[dict[str, str]]) -> str:
    attributes = {
        "links": links,
    }

    return render_template("components/admin/aside_menu.html", attributes=attributes)
