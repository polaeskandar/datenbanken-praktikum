from flask_login import current_user
from flask_sqlalchemy.query import Query
from sqlalchemy import or_, case

from app.dto.RestaurantSearchContext import RestaurantSearchContext
from app.models.PostalCode import PostalCode
from app.models.PostalCodeRestaurant import PostalCodeRestaurant
from app.models.Restaurant import Restaurant


class RestaurantSearchService:
    def __init__(self, context: RestaurantSearchContext):
        self.context = context

    def fetch_restaurants(self):
        query = Restaurant.query
        search_conditions = self.get_search_terms_conditions()

        # 1. Filter by search terms
        if search_conditions:
            query = query.filter(or_(*search_conditions))

        # 2. Sort by proximity to the user's main postal code (if available)
        query = self.apply_postal_code_sort(query)

        # TODO 3. Sort by opening hours to be implemented

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
    # Sorting by Proximity
    # --------------------------------------------------------------
    # Simple algorithm for sorting by the absolute difference
    # between the postal code of the user and the postal code
    # of the restaurants.
    # --------------------------------------------------------------
    def apply_postal_code_sort(self, query: Query):
        user_postal_code = current_user.postal_code.postal_code or None

        if not user_postal_code:
            return query

        query = (
            query.join(PostalCodeRestaurant, isouter=True)
            .join(PostalCode, isouter=True)
            .order_by(
                case((PostalCode.postal_code == user_postal_code, 0), else_=1),
                PostalCodeRestaurant.distance.asc(),
            )
        )

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

    def get_postal_codes_as_list(self) -> list[str]:
        if not self.context.postal_codes:
            return []

        codes = {
            code.strip().lower()
            for code in self.context.postal_codes.split(",")
            if code.strip()
        }

        return list(codes)
