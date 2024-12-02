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
        back_populates="restaurants",
        cascade="all, delete-orphan",
    )
