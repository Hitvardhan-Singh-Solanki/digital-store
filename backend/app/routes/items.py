from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import json
from models import Item
from schemas import ItemResponse
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
