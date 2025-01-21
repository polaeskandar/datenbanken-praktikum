from datetime import datetime

from flask_login import current_user
from flask_sqlalchemy.query import Query
from sqlalchemy import or_, case, asc, func, cast, Integer

from app.dto.RestaurantSearchContext import RestaurantSearchContext
from app.models.OpeningHour import OpeningHour
from app.models.PostalCode import PostalCode
from app.models.PostalCodeRestaurant import PostalCodeRestaurant
from app.models.Restaurant import Restaurant


class RestaurantSearchService:
    def __init__(self, context: RestaurantSearchContext):
        self.context = context

    def fetch_restaurants(self) -> list[Restaurant]:
        query = Restaurant.query
        search_conditions = self.get_search_terms_conditions()

        # 1. Filter by search terms
        if search_conditions:
            query = query.filter(or_(*search_conditions))

        # 2. Sort by opening hours to be implemented
        query = self.apply_opening_hours_sort(query)

        # 3. Sort by distance to user's district
        query = self.apply_postal_code_sort(query)

        return query.all()

    # --------------------------------------------------------------
    # Filtering by Name/Description
    # --------------------------------------------------------------
    def get_search_terms_conditions(self) -> list:
        restaurant_names_list = self.get_restaurant_names_as_list()

        if len(restaurant_names_list) == 0:
            return []

        conditions = []

        for term in restaurant_names_list:
            like_pattern = f"%{term}%"
            conditions.append(Restaurant.name.ilike(like_pattern))
            conditions.append(Restaurant.description.ilike(like_pattern))

        return conditions

    # --------------------------------------------------------------
    # Sort by "Currently Open" (open first)
    # --------------------------------------------------------------
    def apply_opening_hours_sort(self, query: Query) -> Query:
        # 1) Grab current day/time in 24-hour format
        now = datetime.now()
        current_day = now.strftime("%A").upper()  # e.g. "MONDAY"
        current_time_str = now.strftime("%H:%M")  # e.g. "09:35"

        # 2) Build a CASE
        is_open_case = case(
            (
                (OpeningHour.day_of_week == current_day)
                & (OpeningHour.opening_time <= current_time_str)
                & (OpeningHour.closing_time >= current_time_str),
                0,
            ),
            else_=1,
        )

        # 3) Outer-join to OpeningHour.
        query = query.outerjoin(OpeningHour, OpeningHour.restaurant_id == Restaurant.id)

        # 4) Sort by:
        query = query.order_by(asc(is_open_case))

        return query

    # --------------------------------------------------------------
    # Sorting by Numerical Difference in Postal Codes
    # --------------------------------------------------------------
    # We convert the user's postal code to an integer, and do the same
    # for each restaurant's postal code (assuming it is stored as a string).
    # We then compute the absolute difference between the two.
    #
    # The result is that restaurants with the same postal code
    # (difference = 0) will appear first, and others follow in ascending
    # order of how close their postal code is numerically to the user's.
    # --------------------------------------------------------------
    def apply_postal_code_sort(self, query: Query) -> Query:
        user_postal_code = current_user.postal_code.postal_code

        if not user_postal_code:
            return query

        user_postal_code = int(user_postal_code)

        query = query.join(PostalCodeRestaurant, isouter=True).join(
            PostalCode, isouter=True
        )

        pc_difference = func.abs(
            cast(PostalCode.postal_code, Integer) - user_postal_code
        )

        query = query.order_by(pc_difference.asc())

        return query

    # --------------------------------------------------------------
    # Parsing Comma-Separated Inputs
    # unique terms -> set()
    # strip, lower, remove empties.
    # --------------------------------------------------------------
    def get_restaurant_names_as_list(self) -> list[str]:
        if not self.context.restaurant_names:
            return []

        names = {
            name.strip().lower()
            for name in self.context.restaurant_names.split(",")
            if name.strip()
        }

        return list(names)
