import random

from faker import Faker

from app import db, app
from app.enum.AccountType import AccountType
from app.models.Account import Account

fake = Faker()


def load_account_fixtures():
    platform_account = Account(
        type=AccountType.PLATFORM,
        email="platform@lieferspatz.com",
        hashed_password="password",
    )

    # 20 Customer and restaurant accounts
    accounts = []

    for _ in range(10):
        accounts.append(
            Account(
                type=AccountType.CUSTOMER,
                email=fake.unique.email(),
                hashed_password="password",
                address=fake.address(),
                balance=round(random.uniform(10.0, 200.0), 2),
                postal_code_id=random.randint(1, 50),
            )
        )

    for _ in range(10):
        accounts.append(
            Account(
                type=AccountType.RESTAURANT,
                email=fake.unique.email(),
                hashed_password="password",
                address=fake.address(),
                balance=round(random.uniform(10.0, 200.0), 2),
                postal_code_id=random.randint(1, 50),
            )
        )

    with app.app_context():
        db.session.add(platform_account)
        db.session.add_all(accounts)
        db.session.commit()

        print("Accounts fixtures loaded successfully.")
