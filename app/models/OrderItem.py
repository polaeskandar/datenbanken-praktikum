from app import db


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_item.id"))

    # Relationships
    order = db.relationship("Order", back_populates="order_items")
    item = db.relationship("MenuItem", back_populates="order_items", uselist=False)
