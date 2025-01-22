from flask_wtf import FlaskForm
from wtforms.fields.numeric import DecimalField
from wtforms.validators import DataRequired, NumberRange


class RateOrderForm(FlaskForm):
    rating = DecimalField(
        "Rating", validators=[DataRequired(), NumberRange(min=1, max=5)]
    )
