from wtforms.fields.simple import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.form.FileAttachedForm import FileAttachedForm
from app.models.Account import Account


class CreateRestaurantForm(FileAttachedForm):
    def __init__(self, *args, **kwargs):
        super(CreateRestaurantForm, self).__init__(
            *args,
            label="Restaurant's Image",
            allowed_extensions=["jpg", "png"],
            **kwargs
        )

    name = StringField(
        "Restaurant name", validators=[DataRequired(), Length(min=3, max=255)]
    )

    address = StringField("Address", validators=[DataRequired()])

    postal_code = StringField("Postal code", validators=[DataRequired()])

    description = TextAreaField("Description", validators=[DataRequired()])

    email = StringField("Email address", validators=[DataRequired(), Email()])

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=255)]
    )

    password_confirm = PasswordField(
        "Password Confirm",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()

        if account is not None:
            raise ValidationError("Account already exists with the same email.")
