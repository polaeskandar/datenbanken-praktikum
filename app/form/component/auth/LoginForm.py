from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError

from app.models.Account import Account


class LoginForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()

        if account is None:
            raise ValidationError("No account found with that email.")
