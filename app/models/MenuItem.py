from sqlalchemy import UniqueConstraint

from app import db


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"), nullable=False)

    __table_args__ = (UniqueConstraint("name", "menu_id", name="uix_name_menu"),)

    # Relationships
    menu = db.relationship("Menu", back_populates="items", uselist=False)
    order_items = db.relationship(
        "OrderItem", back_populates="item", lazy="dynamic", cascade="all, delete-orphan"
    )
    carts = db.relationship("CartItem", back_populates="item")
