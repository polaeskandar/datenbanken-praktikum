from app import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), unique=True)

    # Relationships
    account = db.relationship("Account", back_populates="customer")
    orders = db.relationship(
        "Order", back_populates="customer", lazy="dynamic", cascade="all, delete-orphan"
    )
