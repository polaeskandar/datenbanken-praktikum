from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Regexp, Optional


class RestaurantsFilterForm(FlaskForm):
    class Meta:
        csrf = False

    postal_codes = StringField(
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

    search_terms = StringField(
        "Search Restaurants",
        validators=[
            Optional(),
        ],
        render_kw={
            "class": "search-input form-control flex-grow-1",
            "placeholder": "Search... e.g. Pizza, Burgers",
        },
    )
