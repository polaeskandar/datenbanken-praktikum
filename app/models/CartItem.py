from app import db


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_item.id"), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)

    # Relationships
    item = db.relationship("MenuItem", back_populates="carts", uselist=False)
    cart = db.relationship("Cart", back_populates="items", uselist=False)
