from wtforms.fields.simple import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from app.form.FileAttachedForm import FileAttachedForm


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

    postal_code = StringField("Postal code", validators=[DataRequired()])

    restaurant_description = TextAreaField(
        "Restaurant's description",
        validators=[DataRequired()],
        render_kw={"rows": 10},
    )
