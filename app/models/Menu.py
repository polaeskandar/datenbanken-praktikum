from enum import unique

from app import db


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id"), unique=True, nullable=False
    )

    # Relationships
    restaurant = db.relationship("Restaurant", back_populates="menu", uselist=False)
    items = db.relationship(
        "MenuItem", back_populates="menu", lazy="dynamic", cascade="all, delete-orphan"
    )
