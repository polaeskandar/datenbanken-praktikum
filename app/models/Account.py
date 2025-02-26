from flask_login import UserMixin

from app import db, login_manager, bcrypt
from app.enum.AccountType import AccountType


class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(AccountType))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    balance = db.Column(db.Float, nullable=False, default=100.0)
    postal_code_id = db.Column(
        db.Integer, db.ForeignKey("postal_code.id"), nullable=True
    )

    # Relationships
    postal_code = db.relationship(
        "PostalCode", back_populates="accounts", uselist=False
    )
    customer = db.relationship("Customer", back_populates="account", uselist=False)
    restaurant = db.relationship("Restaurant", back_populates="account", uselist=False)
    notifications = db.relationship(
        "Notification", back_populates="account", uselist=True
    )

    def is_customer(self):
        return self.get_account_type() == AccountType.CUSTOMER

    def is_restaurant(self):
        return self.get_account_type() == AccountType.RESTAURANT

    def is_platform(self):
        return self.get_account_type() == AccountType.PLATFORM

    def get_account_type(self) -> AccountType:
        if self.type == AccountType.CUSTOMER:
            return AccountType.CUSTOMER

        if self.type == AccountType.RESTAURANT:
            return AccountType.RESTAURANT

        if self.type == AccountType.PLATFORM:
            return AccountType.PLATFORM

        raise Exception("Invalid account type, both customer and restaurant are None.")

    @property
    def hashed_password(self):
        return self.password

    @hashed_password.setter
    def hashed_password(self, plain_password):
        self.password = bcrypt.generate_password_hash(plain_password).decode("utf-8")

    def verify_password(self, plain_password):
        return bcrypt.check_password_hash(self.hashed_password, plain_password)


@login_manager.user_loader
def load_account(account_id) -> Account:
    return Account.query.get(int(account_id))
