from app import db


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id"), nullable=False
    )

    # Relationship
    customer = db.relationship("Customer", back_populates="carts", uselist=False)
    restaurant = db.relationship("Restaurant", back_populates="carts", uselist=False)
    items = db.relationship("CartItem", back_populates="cart")
