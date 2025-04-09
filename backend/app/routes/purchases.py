from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Purchase, Item, User
from schemas import PurchaseResponse, PurchaseCreate
from database import get_db

router = APIRouter(prefix="/api/purchases", tags=["purchases"])


@router.get("/", response_model=List[PurchaseResponse])
async def get_purchases(user_id: str = None, db: Session = Depends(get_db)):
    if not user_id:
        return []

    purchases = db.query(Purchase).filter(Purchase.user_id == user_id).all()
    purchase_responses = []
    for purchase in purchases:
        item = db.query(Item).filter(Item.id == purchase.item_id).first()
        purchase_responses.append(
            {
                "id": purchase.id,
                "user_id": purchase.user_id,
                "item": item,
                "timestamp": purchase.timestamp,
                "order_id": purchase.order_id,
            }
        )
    return purchase_responses


@router.post("/", response_model=PurchaseResponse)
async def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == purchase.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    user = db.query(User).filter(User.id == purchase.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_purchase = Purchase(item_id=purchase.item_id, user_id=purchase.user_id)
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    return {
        "id": new_purchase.id,
        "user_id": new_purchase.user_id,
        "item": item,
        "timestamp": new_purchase.timestamp,
        "order_id": new_purchase.order_id,
    }
