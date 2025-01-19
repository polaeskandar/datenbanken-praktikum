from app import db, app
from app.enum.AccountType import AccountType
from app.models.Account import Account


def load_account_fixtures():
    account = Account(
        type=AccountType.PLATFORM,
        email="platform@lieferspatz.com",
        hashed_password="password",
    )

    with app.app_context():
        db.session.add_all([account])
        db.session.commit()
