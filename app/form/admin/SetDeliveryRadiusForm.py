from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField
from wtforms.validators import DataRequired, NumberRange


class SetDeliveryRadiusForm(FlaskForm):
    postal_code = StringField("Postal code", validators=[DataRequired()])

    distance = DecimalField(
        validators=[
            DataRequired(),
            NumberRange(min=0, message="Distance must be positive."),
        ],
        places=2,
    )
