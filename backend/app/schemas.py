from pydantic import BaseModel
from datetime import datetime


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True


class PurchaseResponse(BaseModel):
    id: int
    user_id: int
    item_id: int
    timestamp: datetime
    order_id: str

    class Config:
        orm_mode = True
