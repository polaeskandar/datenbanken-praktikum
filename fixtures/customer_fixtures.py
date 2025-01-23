from faker import Faker

from app import app, db
from app.enum.AccountType import AccountType
from app.models.Account import Account
from app.models.Customer import Customer

fake = Faker()


def load_customer_fixtures():
    with app.app_context():
        accounts = Account.query.filter_by(type=AccountType.CUSTOMER).all()

        if len(accounts) < 10:
            print(
                "Not enough accounts to assign to customers. Please add more accounts."
            )

            return

        # Generate 10 customers
        customers = []

        for i in range(10):
            customer = Customer(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                account_id=accounts[i].id,  # Assign each customer to an account
            )

            customers.append(customer)

        db.session.add_all(customers)
        db.session.commit()

        print("10 customer fixtures loaded successfully.")
