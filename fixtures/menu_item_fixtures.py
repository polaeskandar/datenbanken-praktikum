import random

from faker import Faker

from app import db, app
from app.models.Menu import Menu
from app.models.MenuItem import MenuItem

fake = Faker()


def load_menu_item_fixtures():
    with app.app_context():
        menus = Menu.query.all()

        if not menus:
            print("No menus found in the database. Please add menus first.")

            return

        menu_items = []

        for menu in menus:
            for i in range(random.randint(5, 10)):
                menu_items.append(
                    MenuItem(
                        name=fake.unique.word().capitalize(),
                        image=f"https://placehold.co/1920x1080?text=Item+{i+1}",
                        price=round(random.uniform(5.0, 50.0), 2),
                        description=fake.text(max_nb_chars=200),
                        menu_id=menu.id,
                    )
                )

        # Add menu items to the database
        db.session.add_all(menu_items)
        db.session.commit()

        print(f"{len(menu_items)} menu items loaded successfully.")
