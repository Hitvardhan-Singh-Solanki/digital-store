from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from datetime import datetime
from db.base import Base


class PendingPurchase(Base):
    __tablename__ = "pending_purchases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    order_id = Column(String, unique=True)
