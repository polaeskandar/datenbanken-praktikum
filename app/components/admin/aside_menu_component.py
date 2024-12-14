from flask import render_template, url_for, request


def aside_menu_component():
    attributes = {
        "links": get_links(),
    }

    return render_template("components/admin/aside_menu.html", attributes=attributes)


def get_links() -> list[dict[str, str]]:
    return [
        {
            "icon": "fa-solid fa-utensils me-2",
            "text": "Menu",
            "href": "#",
            "is_active": False,
        },
        {
            "icon": "fa-solid fa-receipt me-2",
            "text": "Orders",
            "href": "#",
            "is_active": False,
        },
        {
            "icon": "fa-solid fa-clock me-2",
            "text": "Opening Hours",
            "href": url_for("admin.opening_hours"),
            "is_active": request.path == url_for('admin.opening_hours'),
        },
        {
            "icon": "fa-solid fa-truck me-2",
            "text": "Delivery Radius",
            "href": url_for("admin.delivery_radius"),
            "is_active": request.path == url_for('admin.delivery_radius'),
        },
        {
            "icon": "fa-solid fa-gears me-2",
            "text": "Settings",
            "href": url_for("admin.settings"),
            "is_active": request.path == url_for('admin.settings'),
        },
    ]
