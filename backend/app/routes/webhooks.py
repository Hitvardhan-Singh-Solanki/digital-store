from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
import json
import hmac
import hashlib
import os

from models import Purchase
from database import get_db

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("/payment")
async def payment_webhook(
    request: Request,
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    body = await request.body()

    secret = os.getenv("XSOLLA_WEBHOOK_SECRET").encode()
    expected_signature = hmac.new(secret, body, hashlib.sha1).hexdigest()

    if authorization != f"Signature {expected_signature}":
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = json.loads(body)
    order_id = data.get("notification_type")
    user_id = data.get("user", {}).get("id")
    item_id = data.get("purchase", {}).get("virtual_item", {}).get("sku")

    if not all([order_id, user_id, item_id]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    existing_purchase = db.query(Purchase).filter_by(order_id=order_id).first()
    if existing_purchase:
        raise HTTPException(status_code=409, detail="Duplicate order")

    purchase = Purchase(user_id=user_id, item_id=item_id, order_id=order_id)
    db.add(purchase)
    db.commit()

    return {"status": "success"}
