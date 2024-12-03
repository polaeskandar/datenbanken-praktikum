from app import db


class PostalCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postal_code = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    accounts = db.relationship("Account", back_populates="postal_code")
    restaurants = db.relationship(
        "PostalCodeRestaurant",
        back_populates="postal_codes",
        cascade="all, delete-orphan",
    )
