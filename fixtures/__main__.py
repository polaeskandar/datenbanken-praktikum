from fixtures.account_fixtures import load_account_fixtures
from fixtures.customer_fixtures import load_customer_fixtures
from fixtures.menu_item_fixtures import load_menu_item_fixtures
from fixtures.opening_hour_fixtures import load_opening_hours_fixtures
from fixtures.postal_code_fixtures import load_postal_code_fixtures
from fixtures.postal_code_restaurant_fixtures import (
    load_postal_code_restaurant_fixtures,
)
from fixtures.restaurant_fixtures import load_restaurant_fixtures

if __name__ == "__main__":
    load_postal_code_fixtures()
    load_account_fixtures()
    load_restaurant_fixtures()
    load_customer_fixtures()
    load_menu_item_fixtures()
    load_opening_hours_fixtures()
    load_postal_code_restaurant_fixtures()
