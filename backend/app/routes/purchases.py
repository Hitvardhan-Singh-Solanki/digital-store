from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Purchase
from schemas import (
    PurchaseResponse,
)
from database import get_db

router = APIRouter(prefix="/api/purchases", tags=["purchases"])


@router.get("/", response_model=List[PurchaseResponse])
async def get_purchases(db: Session = Depends(get_db)):
    purchases = db.query(Purchase).all()
    return purchases
