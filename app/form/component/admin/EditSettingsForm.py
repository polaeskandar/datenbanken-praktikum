from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditSettingsForm(FlaskForm):
    restaurant_name = StringField(
        "Restaurant's name", validators=[DataRequired(), Length(min=3, max=255)]
    )

    address = StringField("Address", validators=[DataRequired()])

    postal_code = SelectField(
        choices=[("", "Choose a postal code")], validators=[DataRequired()]
    )

    restaurant_description = TextAreaField(
        "Restaurant's description",
        validators=[DataRequired()],
        render_kw={"rows": 10},
    )

    image = FileField("Image", validators=[FileAllowed(["jpg", "png"])])
