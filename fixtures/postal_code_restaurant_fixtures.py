import random

from app import db, app
from app.models.PostalCode import PostalCode
from app.models.PostalCodeRestaurant import PostalCodeRestaurant
from app.models.Restaurant import Restaurant


def load_postal_code_restaurant_fixtures():
    with app.app_context():
        # Fetch all restaurants and postal codes from the database
        restaurants = Restaurant.query.all()
        postal_codes = PostalCode.query.all()

        if not restaurants:
            print("No restaurants found in the database. Please add restaurants first.")
            return

        if not postal_codes:
            print(
                "No postal codes found in the database. Please add postal codes first."
            )
            return

        postal_code_restaurant_entries = []
        for restaurant in restaurants:
            # Assign random postal codes to each restaurant (3-5 per restaurant)
            assigned_postal_codes = random.sample(postal_codes, k=random.randint(3, 5))

            for postal_code in assigned_postal_codes:
                postal_code_restaurant = PostalCodeRestaurant(
                    distance=round(
                        random.uniform(0.0, 15.0), 2
                    ),  # Random distance between 0.0 and 15.0 km
                    restaurant_id=restaurant.id,
                    postal_code_id=postal_code.id,
                )
                postal_code_restaurant_entries.append(postal_code_restaurant)

        # Add all entries to the database
        db.session.add_all(postal_code_restaurant_entries)
        db.session.commit()

        print(f"Postal code entries loaded for {len(restaurants)} restaurants.")
