from datetime import datetime

from app import db


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), unique=True)

    # Relationships
    account = db.relationship("Account", back_populates="restaurant")
    orders = db.relationship(
        "Order",
        back_populates="restaurant",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    menu = db.relationship(
        "Menu", back_populates="restaurant", cascade="all, delete-orphan", uselist=False
    )
    opening_hours = db.relationship(
        "OpeningHour",
        back_populates="restaurant",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    postal_codes = db.relationship(
        "PostalCodeRestaurant",
        back_populates="restaurant",
        cascade="all, delete-orphan",
    )
    carts = db.relationship(
        "Cart",
        back_populates="restaurant",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def is_currently_open(self) -> bool:
        now = datetime.now()
        current_day = now.strftime("%A").upper()  # e.g. "MONDAY"
        current_time_str = now.strftime("%H:%M")  # e.g. "09:35"

        for opening_hour in self.opening_hours.all():
            if opening_hour.day_of_week.name == current_day:
                if (
                    opening_hour.opening_time
                    <= current_time_str
                    <= opening_hour.closing_time
                ):
                    return True

        return False
