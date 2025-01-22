from datetime import datetime, UTC

from app import db
from app.enum.OrderStatus import OrderStatus


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(OrderStatus), nullable=False)
    price = db.Column(db.Float, nullable=False)
    wishes_text = db.Column(db.Text, nullable=True)
    ordered_at = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))
    rating = db.Column(db.Float, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id"), nullable=False
    )

    # Relationships
    customer = db.relationship("Customer", back_populates="orders", uselist=False)
    restaurant = db.relationship("Restaurant", back_populates="orders", uselist=False)
    order_items = db.relationship(
        "OrderItem",
        back_populates="order",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
