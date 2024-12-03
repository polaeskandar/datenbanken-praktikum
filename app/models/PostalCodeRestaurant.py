from app import db


class PostalCodeRestaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # The distance is in KM, 0.0 means it is in the same district
    distance = db.Column(db.Float, nullable=False, default=0.0)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id"), nullable=False
    )
    postal_code_id = db.Column(
        db.Integer, db.ForeignKey("postal_code.id"), nullable=False
    )

    # Relationships
    restaurants = db.relationship("Restaurant", back_populates="postal_codes")
    postal_codes = db.relationship("PostalCode", back_populates="restaurants")
