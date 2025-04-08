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
    user_id: int
    item_id: int
    timestamp: datetime
    order_id: str

    class Config:
        from_attributes = True
