from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models.Account import Account


class RegisterCustomerForm(FlaskForm):
    first_name = StringField(
        "First name", validators=[DataRequired(), Length(min=3, max=255)]
    )

    last_name = StringField(
        "Last name", validators=[DataRequired(), Length(min=3, max=255)]
    )

    email = StringField("Email address", validators=[DataRequired(), Email()])

    address = StringField("Address", validators=[DataRequired()])

    postal_code = StringField("Postal code", validators=[DataRequired()])

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
