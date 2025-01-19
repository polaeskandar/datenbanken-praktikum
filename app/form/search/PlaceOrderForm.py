from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import Optional


class PlaceOrderForm(FlaskForm):
    wishes_text = TextAreaField(
        "Any wishes to your order? Add them here!",
        validators=[Optional()],
        render_kw={"class": "text-muted", "rows": "10"},
    )
