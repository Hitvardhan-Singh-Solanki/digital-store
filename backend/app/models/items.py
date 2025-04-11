from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
)
from db.base import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
