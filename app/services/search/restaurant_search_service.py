from sqlalchemy import or_

from app.dto.RestaurantSearchContext import RestaurantSearchContext
from app.models.Account import Account
from app.models.PostalCode import PostalCode
from app.models.Restaurant import Restaurant


class RestaurantSearchService:
    def __init__(self, context: RestaurantSearchContext):
        self.context = context

    def fetch_restaurants(self):
        query = Restaurant.query
        search_conditions = self.get_search_terms_conditions()

        if len(search_conditions) > 0:
            query = query.filter(or_(*search_conditions))

        query = self.apply_postal_codes_filter(query)

        return query.all()

    def get_search_terms_conditions(self) -> list[str]:
        restaurant_names_list = self.get_restaurant_names_as_list()

        if restaurant_names_list is None or len(restaurant_names_list) == 0:
            return []

        conditions = []

        for term in restaurant_names_list:
            like_pattern = f"%{term}%"
            conditions.append(Restaurant.name.ilike(like_pattern))
            conditions.append(Restaurant.description.ilike(like_pattern))

        return conditions

    def apply_postal_codes_filter(self, query):
        postal_codes_list = self.get_postal_codes_as_list()

        if postal_codes_list is None or len(postal_codes_list) == 0:
            return query

        query = (
            query.join(Restaurant.account)
            .join(Account.postal_code)
            .filter(PostalCode.postal_code.in_(postal_codes_list))
        )

        return query

    def get_restaurant_names_as_list(self) -> list[str] | None:
        if self.context.restaurant_names is None:
            return None

        return [
            item
            for item in [
                name.strip().lower() or None
                for name in list(set(self.context.restaurant_names.split(",")))
            ]
            if item is not None
        ]

    def get_postal_codes_as_list(self) -> list[str] | None:
        if self.context.postal_codes is None:
            return None

        return [
            item
            for item in [
                postal_code.strip().lower() or None
                for postal_code in list(set(self.context.postal_codes.split(",")))
            ]
            if item is not None
        ]
