from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from app.form.component.FileAttachedForm import FileAttachedForm


class EditSettingsForm(FileAttachedForm):
    def __init__(self, *args, **kwargs):
        super(EditSettingsForm, self).__init__(
            *args,
            label="Restaurant's Image",
            allowed_extensions=["jpg", "png"],
            **kwargs
        )

    restaurant_name = StringField(
        "Restaurant's name", validators=[DataRequired(), Length(min=3, max=255)]
    )

    address = StringField("Address", validators=[DataRequired()])

    postal_code = SelectField(
        choices=[("", "Choose a postal code")],
    )

    new_postal_code = StringField(
        "New Postal Code", validators=[Length(min=3, max=255)],
        render_kw={"placeholder": "Fill if you didn't find your postal code in the select box above"},
    )

    restaurant_description = TextAreaField(
        "Restaurant's description",
        validators=[DataRequired()],
        render_kw={"rows": 10},
    )