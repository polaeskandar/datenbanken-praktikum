from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_account(account_id):
    return Account.query.get(int(account_id))


class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    balance = db.Column(db.Float, nullable=False, default=100.0)
