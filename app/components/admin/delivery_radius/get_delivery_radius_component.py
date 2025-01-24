from flask import render_template
from flask_login import current_user

from app.models.PostalCode import PostalCode
from app.models.PostalCodeRestaurant import PostalCodeRestaurant


def get_delivery_radius_component() -> str:
    postal_codes = (
        PostalCodeRestaurant.query.join(
            PostalCode, PostalCode.id == PostalCodeRestaurant.postal_code_id
        )
        .filter(PostalCodeRestaurant.restaurant_id == current_user.restaurant.id)
        .all()
    )

    attributes = {"postal_codes": postal_codes}

    return render_template(
        "components/admin/delivery_radius/get_delivery_radius.html",
        attributes=attributes,
    )
