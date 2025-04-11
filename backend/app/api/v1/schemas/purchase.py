from api.v1.schemas.item import ItemResponse
from pydantic import BaseModel
from datetime import datetime


class PurchaseResponse(BaseModel):
    id: int
    user_id: str
    item: ItemResponse
    timestamp: datetime
    order_id: str

    class Config:
        from_attributes = True


class PurchaseCreate(BaseModel):
    item_id: int
    user_id: str
