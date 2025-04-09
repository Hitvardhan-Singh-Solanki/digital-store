from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int


class PurchaseResponse(BaseModel):
    id: int
    user_id: str
    item_id: int
    timestamp: datetime
    order_id: str

    class Config:
        from_attributes = True


class PurchaseCreate(BaseModel):
    item_id: int
    user_id: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str

    class Config:
        orm_mode = True


class UserDeleteRequest(BaseModel):
    password: str
