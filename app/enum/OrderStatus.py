from enum import Enum


class OrderStatus(Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
