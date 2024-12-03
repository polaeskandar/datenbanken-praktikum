INSERT INTO postal_code (postal_code)
VALUES
    ('10115'),
    ('10249'),
    ('10365'),
    ('10435'),
    ('10585'),
    ('10623'),
    ('10789'),
    ('10827'),
    ('10965'),
    ('11011');

INSERT INTO account (email, password, address, balance, postal_code_id)
VALUES
    ('john.doe@example.com', 'hashed_password1', '123 Elm Street', 100.0, 1),
    ('jane.smith@example.com', 'hashed_password2', '456 Oak Avenue', 100.0, 2),
    ('robert.brown@example.com', 'hashed_password3', '789 Pine Road', 100.0, 3),
    ('emily.jones@example.com', 'hashed_password4', '321 Maple Lane', 100.0, 4),
    ('william.davis@example.com', 'hashed_password5', '654 Birch Drive', 100.0, 5),
    ('sophia.miller@example.com', 'hashed_password6', '987 Cedar Street', 100.0, 6),
    ('james.wilson@example.com', 'hashed_password7', '111 Spruce Circle', 100.0, 7),
    ('isabella.moore@example.com', 'hashed_password8', '222 Chestnut Way', 100.0, 8),
    ('michael.taylor@example.com', 'hashed_password9', '333 Walnut Place', 100.0, 9),
    ('olivia.anderson@example.com', 'hashed_password10', '444 Ash Court', 100.0, 10);
INSERT INTO account (email, password, address, balance, postal_code_id)
VALUES
    ('italian.bistro@example.com', 'hashed_password11', '1 Little Italy St', 100.0, 1),
    ('golden.dragon@example.com', 'hashed_password12', '2 Chinatown Blvd', 100.0, 2),
    ('sunrise.cafe@example.com', 'hashed_password13', '3 Morning Lane', 100.0, 3),
    ('bbq.heaven@example.com', 'hashed_password14', '4 Smokehouse Dr', 100.0, 4),
    ('sushi.master@example.com', 'hashed_password15', '5 Sakura Rd', 100.0, 5),
    ('green.garden@example.com', 'hashed_password16', '6 Vegan Way', 100.0, 6),
    ('burger.shack@example.com', 'hashed_password17', '7 Grill Avenue', 100.0, 7),
    ('royal.tandoor@example.com', 'hashed_password18', '8 Spice Street', 100.0, 8),
    ('pizza.palace@example.com', 'hashed_password19', '9 Mozzarella Ct', 100.0, 9),
    ('french.corner@example.com', 'hashed_password20', '10 Parisian Rd', 100.0, 10);
INSERT INTO customer (first_name, last_name, account_id)
VALUES
    ('John', 'Doe', 1),
    ('Jane', 'Smith', 2),
    ('Robert', 'Brown', 3),
    ('Emily', 'Jones', 4),
    ('William', 'Davis', 5),
    ('Sophia', 'Miller', 6),
    ('James', 'Wilson', 7),
    ('Isabella', 'Moore', 8),
    ('Michael', 'Taylor', 9),
    ('Olivia', 'Anderson', 10);
INSERT INTO restaurant (name, description, account_id)
VALUES
    ('Italian Bistro', 'Authentic Italian cuisine with a modern twist.', 11),
    ('Golden Dragon', 'Traditional Chinese flavors served fresh.', 12),
    ('Sunrise Cafe', 'A cozy spot for breakfast and brunch.', 13),
    ('BBQ Heaven', 'The best smoked meats in town.', 14),
    ('Sushi Master', 'Exquisite sushi prepared by skilled chefs.', 15),
    ('Green Garden', 'Delicious vegan and vegetarian dishes.', 16),
    ('Burger Shack', 'Classic burgers made with fresh ingredients.', 17),
    ('Royal Tandoor', 'Aromatic Indian cuisine from the heart.', 18),
    ('Pizza Palace', 'Wood-fired pizzas with gourmet toppings.', 19),
    ('French Corner', 'Fine dining inspired by French traditions.', 20);
INSERT INTO postal_code_restaurant (restaurant_id, postal_code_id, distance)
VALUES
    (11, 1, 0.5),
    (11, 2, 2.0),
    (12, 3, 1.0),
    (12, 4, 2.5),
    (13, 5, 0.0),
    (14, 6, 1.0),
    (14, 7, 2.0),
    (15, 8, 0.0),
    (16, 9, 1.5),
    (17, 10, 3.0),
    (18, 1, 4.0),
    (19, 2, 3.5),
    (20, 4, 2.0);
INSERT INTO opening_hour (day_of_week, opening_time, closing_time, restaurant_id)
VALUES
    ('Monday', '10:00', '22:00', 11),
    ('Tuesday', '10:00', '22:00', 11),
    ('Wednesday', '10:00', '22:00', 11),
    ('Thursday', '10:00', '22:00', 11),
    ('Friday', '10:00', '23:00', 11),
    ('Saturday', '11:00', '23:00', 11),
    ('Sunday', '12:00', '21:00', 11),
    ('Monday', '11:00', '22:30', 12),
    ('Tuesday', '11:00', '22:30', 12),
    ('Wednesday', '11:00', '22:30', 12),
    ('Thursday', '11:00', '22:30', 12),
    ('Friday', '11:00', '23:30', 12),
    ('Saturday', '12:00', '23:30', 12),
    ('Sunday', '12:00', '21:00', 12),
    ('Monday', '07:00', '15:00', 13),
    ('Tuesday', '07:00', '15:00', 13),
    ('Wednesday', '07:00', '15:00', 13),
    ('Thursday', '07:00', '15:00', 13),
    ('Friday', '07:00', '15:00', 13),
    ('Saturday', '08:00', '16:00', 13),
    ('Sunday', '08:00', '16:00', 13),
    ('Monday', '11:00', '22:00', 14),
    ('Tuesday', '11:00', '22:00', 14),
    ('Wednesday', '11:00', '22:00', 14),
    ('Thursday', '11:00', '22:00', 14),
    ('Friday', '11:00', '23:00', 14),
    ('Saturday', '12:00', '23:00', 14),
    ('Sunday', '12:00', '21:00', 14);

INSERT INTO menu (restaurant_id)
VALUES
    (11),
    (12),
    (13),
    (14),
    (15),
    (16),
    (17),
    (18),
    (19),
    (20);

INSERT INTO menu_item (name, image, price, description, menu_id)
VALUES
    ('Margherita Pizza', '/images/margherita.jpg', 8.99, 'Classic pizza with tomato sauce and mozzarella.', 1),
    ('Spaghetti Carbonara', '/images/carbonara.jpg', 12.99, 'Pasta with pancetta, eggs, and parmesan.', 1),
    ('Tiramisu', '/images/tiramisu.jpg', 5.99, 'Traditional Italian dessert.', 1),
    ('Sweet and Sour Chicken', '/images/sweet_sour.jpg', 10.99, 'Chicken in sweet and sour sauce.', 2),
    ('Spring Rolls', '/images/spring_rolls.jpg', 4.99, 'Vegetarian spring rolls with dipping sauce.', 2),
    ('Fried Rice', '/images/fried_rice.jpg', 8.99, 'Rice with vegetables, egg, and soy sauce.', 2),
    ('Cappuccino', '/images/cappuccino.jpg', 3.50, 'Rich espresso with steamed milk.', 3),
    ('Blueberry Muffin', '/images/muffin.jpg', 2.99, 'Freshly baked muffin with blueberries.', 3),
    ('Avocado Toast', '/images/avocado_toast.jpg', 6.99, 'Toast topped with mashed avocado and seasoning.', 3),
    ('BBQ Ribs', '/images/bbq_ribs.jpg', 18.99, 'Slow-cooked ribs with BBQ sauce.', 4),
    ('Pulled Pork Sandwich', '/images/pulled_pork.jpg', 10.99, 'Sandwich with pulled pork and coleslaw.', 4),
    ('Coleslaw', '/images/coleslaw.jpg', 3.99, 'Creamy coleslaw with cabbage and carrots.', 4);

INSERT INTO cart (note, customer_id, restaurant_id)
VALUES
    ('Extra napkins please.', 1, 11),
    (NULL, 2, 12),
    ('No onions.', 3, 13),
    ('Make it spicy.', 4, 14),
    (NULL, 5, 15),
    ('Include utensils.', 6, 16),
    ('Double the sauce.', 7, 17),
    ('Serve hot.', 8, 18),
    ('Add extra cheese.', 9, 19),
    ('Make it vegan.', 10, 20);

INSERT INTO cart_item (quantity, menu_item_id, cart_id)
VALUES
    (2, 1, 1),
    (1, 2, 1),
    (3, 4, 2),
    (1, 5, 2),
    (1, 8, 3),
    (2, 10, 4),
    (1, 9, 4);

INSERT INTO "order" (status, price, ordered_at, customer_id, restaurant_id)
VALUES
    ('Completed', 25.97, '2024-11-30 12:15:00', 1, 11),
    ('Pending', 29.97, '2024-11-30 13:45:00', 2, 12),
    ('Cancelled', 6.99, '2024-11-29 08:30:00', 3, 13),
    ('Completed', 32.97, '2024-11-28 19:20:00', 4, 14),
    ('Pending', 10.50, '2024-11-30 17:00:00', 5, 15);

INSERT INTO order_menu_item (order_id, menu_item_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 4),
    (2, 5),
    (3, 8),
    (4, 10),
    (4, 9);
