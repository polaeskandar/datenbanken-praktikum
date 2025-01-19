from datetime import datetime, timezone

from app import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)

    # Relationships
    account = db.relationship("Account", back_populates="notifications", uselist=False)
