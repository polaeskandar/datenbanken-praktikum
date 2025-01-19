from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Regexp, Optional


class RestaurantsFilterForm(FlaskForm):
    class Meta:
        csrf = False

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
