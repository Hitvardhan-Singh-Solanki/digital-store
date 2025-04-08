from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import json
from models import Item
from schemas import ItemResponse, ItemCreate
from database import get_db, redis_client

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("/", response_model=List[ItemResponse])
async def get_items(db: Session = Depends(get_db)):
    cached_items = redis_client.get("items")
    if cached_items:
        return json.loads(cached_items)

    items = db.query(Item).all()

    cache_data = [ItemResponse.from_orm(item).dict() for item in items]
    redis_client.setex("items", 300, json.dumps(cache_data))

    return items


@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    redis_client.delete("items")

    return db_item
