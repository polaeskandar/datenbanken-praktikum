from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class MenuItemForm(FlaskForm):
    image = FileField(
        "Image",
        validators=[
            FileAllowed(["jpg", "png"]),
        ],
    )

    item_name = StringField(
        "Item's name", validators=[DataRequired(), Length(min=3, max=255)]
    )

    price = DecimalField("Price", validators=[DataRequired()])

    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw={"rows": 10},
    )
