class RestaurantSearchContext:
    def __init__(self, restaurant_names: str | None, query_sort: str | None):
        self.restaurant_names = restaurant_names
        self.query_sort = query_sort
