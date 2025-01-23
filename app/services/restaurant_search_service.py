from datetime import datetime

from flask_login import current_user
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from sqlalchemy import or_, case, asc, desc, func

from app.dto.RestaurantSearchContext import RestaurantSearchContext
from app.enum.QuerySort import QuerySort
from app.models.OpeningHour import OpeningHour
from app.models.PostalCode import PostalCode
from app.models.Order import Order
from app.models.PostalCodeRestaurant import PostalCodeRestaurant
from app.models.Restaurant import Restaurant
from app.services.pagination_service import paginate_query


class RestaurantSearchService:
    def __init__(self, context: RestaurantSearchContext):
        self.context = context

    def fetch_restaurants(self) -> Pagination:
        query = Restaurant.query
        search_conditions = self.get_search_terms_conditions()

        # 1. Filter by search terms
        if search_conditions:
            query = query.filter(or_(*search_conditions))

        # 2. Sort by opening hours to be implemented
        query = self.apply_opening_hours_sort(query)

        # 3. Sort by distance to user's district
        query = self.apply_postal_code_sort(query)

        # 4. Query sorting options.
        query = self.apply_query_sorting(query)

        # Finally, ensure distinct results
        query = query.distinct(Restaurant.id)

        return paginate_query(query)

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
    # Sort restaurants so that those serving the user's postal code come first,
    # ordered by ascending distance. Restaurants that do not serve the user's code
    # are listed afterwards.
    # --------------------------------------------------------------
    def apply_postal_code_sort(self, query: Query) -> Query:
        if not (current_user.postal_code and current_user.postal_code.postal_code):
            return query

        user_postal_code = current_user.postal_code.postal_code

        query = query.outerjoin(
            PostalCodeRestaurant, PostalCodeRestaurant.restaurant_id == Restaurant.id
        ).outerjoin(PostalCode, PostalCodeRestaurant.postal_code_id == PostalCode.id)

        is_serving_case = case((PostalCode.postal_code == user_postal_code, 0), else_=1)

        query = query.order_by(is_serving_case, PostalCodeRestaurant.distance.asc())

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

    # --------------------------------------------------------------
    # Applying Query Sorting
    # - Alphabetically by name (A–Z)
    # - By the most ordered (descending count of orders)
    # - By average rating (descending)
    # - By newest (most recently created first)
    # --------------------------------------------------------------
    def apply_query_sorting(self, query):
        # 1) Alphabetically by name
        if self.context.query_sort == QuerySort.alphabetically.name:
            return query.order_by(asc(Restaurant.name))

        # 2) By top-ordered (descending count of Orders)
        if self.context.query_sort == QuerySort.top_ordered.name:
            query = query.outerjoin(Order, Order.restaurant_id == Restaurant.id)
            query = query.group_by(Restaurant.id)
            return query.order_by(desc(func.count(Order.id)))

        # 3) By average rating (using the rating field on Order)
        if self.context.query_sort == QuerySort.rating.name:
            query = query.outerjoin(Order, Order.restaurant_id == Restaurant.id)
            query = query.group_by(Restaurant.id)
            average_rating = func.coalesce(func.avg(Order.rating), 0)
            return query.order_by(desc(average_rating))

        # 4) By newest
        if self.context.query_sort == QuerySort.newest.name:
            return query.order_by(desc(Restaurant.created_at))

        return query
