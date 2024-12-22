class RestaurantSearchContext:
    def __init__(self, restaurant_names: str | None, postal_codes: str | None):
        self.restaurant_names = restaurant_names
        self.postal_codes = postal_codes
