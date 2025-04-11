from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.orm import relationship
import uuid
from db.base import Base


class User(Base):
    """
    No Security mechanism whatsoever, this is just a demo
    in order to create a simulation of the user flow.
    NOT TO BE USED EVER IN PRODUCTION CODE.
    """

    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    purchases = relationship(
        "Purchase", back_populates="user", cascade="all, delete-orphan"
    )
