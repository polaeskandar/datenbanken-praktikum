from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Regexp, Optional


class RestaurantsFilterForm(FlaskForm):
    class Meta:
        csrf = False

    postal_code = StringField(
        "Postal code",
        validators=[
            Optional(),
            Regexp(
                r"^\d{5}(?:,\s*\d{5})*$",
                message="Enter valid postal codes, e.g., 47249, 47057.",
            ),
        ],
        render_kw={"class": "form-control", "placeholder": "e.g. 47249, 47057, ..."},
    )

    search_term = StringField(
        "Search Restaurants",
        validators=[
            Optional(),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "Search... e.g. Pizza, Burgers",
        },
    )
