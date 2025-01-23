from faker import Faker

from app import db, app
from app.enum.AccountType import AccountType
from app.models.Account import Account
from app.models.Menu import Menu
from app.models.Restaurant import Restaurant

fake = Faker()


def load_restaurant_fixtures():
    with app.app_context():
        accounts = Account.query.filter_by(type=AccountType.RESTAURANT).all()

        if len(accounts) < 10:
            print(
                "Not enough accounts to assign to restaurants. Please add more accounts."
            )

            return

        # Generate 10 restaurants
        restaurants = []
        menus = []

        for i in range(10):
            restaurant = Restaurant(
                name=fake.company(),
                image=f"https://placehold.co/1920x1080?text=Restaurant+{i+1}",
                description=fake.text(max_nb_chars=200),
                account_id=accounts[i].id,  # Assign each restaurant to an account
                created_at=fake.date_time(),
            )

            menu = Menu(
                restaurant=restaurant,
            )

            restaurants.append(restaurant)
            menus.append(menu)

        # Add to the database
        db.session.add_all(restaurants)
        db.session.add_all(menus)
        db.session.commit()

        print("10 restaurant fixtures loaded successfully.")
