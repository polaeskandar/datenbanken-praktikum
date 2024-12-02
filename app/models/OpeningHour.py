from app import db
from app.enum.DayOfWeek import DayOfWeek


class OpeningHour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)
    opening_time = db.Column(db.String(10), nullable=False)
    closing_time = db.Column(db.String(10), nullable=False)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id"), unique=True, nullable=False
    )

    # Relationships
    restaurant = db.relationship(
        "Restaurant", back_populates="opening_hours", uselist=False
    )
