from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField
from wtforms.fields.datetime import TimeField
from wtforms.validators import DataRequired


# Define a subform for individual days
class DayHoursForm(Form):
    opening_hour = TimeField(
        "Opening Hour",
        format="%H:%M",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )

    closing_hour = TimeField(
        "Closing Hour",
        format="%H:%M",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )


# Main form
class SetOpeningHoursForm(FlaskForm):
    days = FieldList(FormField(DayHoursForm), min_entries=7)
