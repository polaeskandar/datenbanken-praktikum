from flask import render_template, url_for, request


def menu_page_navigation_component() -> str:
    attributes = {"links": get_links()}

    return render_template(
        "components/admin/menu/menu_page_navigation.html", attributes=attributes
    )


def get_links() -> list[dict[str, str]]:
    return [
        {
            "icon": "fa-solid fa-receipt me-2",
            "text": "Menu Overview",
            "href": url_for("admin.menu_overview"),
            "is_active": request.path == url_for("admin.menu_overview"),
        },
        {
            "icon": "fa-solid fa-plus me-2",
            "text": "Add a new Menu Item",
            "href": url_for("admin.add_menu_item"),
            "is_active": request.path == url_for("admin.add_menu_item"),
        },
    ]
