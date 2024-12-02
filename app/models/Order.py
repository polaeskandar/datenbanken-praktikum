from enum import Enum
from datetime import datetime, UTC

from app import db


class OrderStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(OrderStatus), nullable=False)
    price = db.Column(db.Float, nullable=False)
    ordered_at = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id"), nullable=False
    )

    # Relationships
    customer = db.relationship("Customer", back_populates="orders", uselist=False)
    restaurant = db.relationship("Restaurant", back_populates="orders", uselist=False)
