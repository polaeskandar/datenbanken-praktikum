from flask import url_for, request

from app.components.layout.aside_menu_component import aside_menu_component


def get_aside_component_for_admin_board():
    return aside_menu_component(
        [
            {
                "icon": "fa-solid fa-receipt me-2",
                "text": "Orders",
                "href": url_for("admin.index"),
                "is_active": request.path
                in [
                    url_for("admin.index"),
                    "/admin/",
                ],
            },
            {
                "icon": "fa-solid fa-utensils me-2",
                "text": "Menu",
                "href": url_for("admin.menu_overview"),
                "is_active": request.path
                in [
                    url_for("admin.menu_overview"),
                    url_for("admin.add_menu_item"),
                ],
            },
            {
                "icon": "fa-solid fa-clock me-2",
                "text": "Opening Hours",
                "href": url_for("admin.opening_hours"),
                "is_active": request.path == url_for("admin.opening_hours"),
            },
            {
                "icon": "fa-solid fa-truck me-2",
                "text": "Delivery Radius",
                "href": url_for("admin.delivery_radius"),
                "is_active": request.path == url_for("admin.delivery_radius"),
            },
            {
                "icon": "fa-solid fa-gears me-2",
                "text": "Settings",
                "href": url_for("admin.settings"),
                "is_active": request.path == url_for("admin.settings"),
            },
        ]
    )
