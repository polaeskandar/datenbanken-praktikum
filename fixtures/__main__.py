from fixtures.account_fixtures import load_account_fixtures
from fixtures.customer_fixtures import load_customer_fixtures
from fixtures.postal_code_fixtures import load_postal_code_fixtures
from fixtures.restaurant_fixtures import load_restaurant_fixtures

if __name__ == "__main__":
    load_postal_code_fixtures()
    load_account_fixtures()
    load_restaurant_fixtures()
    load_customer_fixtures()
