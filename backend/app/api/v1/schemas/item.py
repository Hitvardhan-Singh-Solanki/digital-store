from pydantic import BaseModel


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
