from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from database import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.now())
    order_id = Column(String, unique=True, default=lambda: str(uuid.uuid4()))

    user = relationship("User", back_populates="purchases")


class PendingPurchase(Base):
    __tablename__ = "pending_purchases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    order_id = Column(String, unique=True)


"""
No Security mechanism whatsoever, this is just a demo
in order to create a simulation of the user flow. 
NOT TO BE USED EVER IN PRODUCTION CODE.
"""


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    purchases = relationship(
        "Purchase", back_populates="user", cascade="all, delete-orphan"
    )
