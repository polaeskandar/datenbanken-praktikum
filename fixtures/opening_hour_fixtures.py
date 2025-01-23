import random

from app import db, app
from app.enum.DayOfWeek import DayOfWeek
from app.models.OpeningHour import OpeningHour
from app.models.Restaurant import Restaurant


def load_opening_hours_fixtures():
    with app.app_context():
        restaurants = Restaurant.query.all()

        if not restaurants:
            print("No restaurants found in the database. Please add restaurants first.")

            return

        opening_hours = []

        for restaurant in restaurants:
            for day in DayOfWeek:
                opening_hour = OpeningHour(
                    day_of_week=day,
                    opening_time=f"{random.randint(8, 11):02d}:00",  # Random opening time between 8:00 and 11:00
                    closing_time=f"{random.randint(18, 22):02d}:00",  # Random closing time between 18:00 and 22:00
                    restaurant_id=restaurant.id,
                )

                opening_hours.append(opening_hour)

        db.session.add_all(opening_hours)
        db.session.commit()

        print(f"Opening hours loaded for {len(restaurants)} restaurants.")
