from app import db


class OrderMenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_item.id"))

    # Relationships
    orders = db.relationship("Order", back_populates="items")
    items = db.relationship("MenuItem", back_populates="orders")
