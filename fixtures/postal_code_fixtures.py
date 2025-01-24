from faker import Faker

from app import db, app
from app.models.PostalCode import PostalCode

fake = Faker()


def load_postal_code_fixtures():
    postal_codes = []

    for _ in range(50):
        postal_codes.append(PostalCode(postal_code=fake.unique.postcode()))

    with app.app_context():
        db.session.add_all(postal_codes)
        db.session.commit()

        print("Postal codes fixtures loaded successfully.")
