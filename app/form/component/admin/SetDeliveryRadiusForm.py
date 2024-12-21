from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class SetDeliveryRadiusForm(FlaskForm):
    postal_code = SelectField(
        choices=[("", "Choose a postal code")], validators=[DataRequired()]
    )

    distance = DecimalField(
        validators=[
            DataRequired(),
            NumberRange(min=0, message="Distance must be positive."),
        ],
        places=2,
    )
