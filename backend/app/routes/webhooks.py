from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
import json
import hmac
import hashlib
import os

from models import Purchase, Item, PendingPurchase
from database import get_db
from main import connected_clients

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


def verify_signature(body: bytes, signature: str, secret: str) -> bool:
    computed = hmac.new(secret.encode(), body, hashlib.sha1).hexdigest()
    return hmac.compare_digest(computed, signature)


@router.post("/payment")
async def payment_webhook(
    request: Request,
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    body = await request.body()

    # Extract signature from Authorization header
    if not authorization or not authorization.startswith("Signature "):
        raise HTTPException(status_code=401, detail="Missing signature")

    signature = authorization.split(" ")[1]
    secret = os.getenv("XSOLLA_WEBHOOK_SECRET", "supersecret")

    # Verify signature
    if not verify_signature(body, signature, secret):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse and validate payload
    try:
        data = json.loads(body)
        if data.get("notification_type") != "payment":
            raise HTTPException(status_code=400, detail="Invalid notification type")

        user_id = data.get("user", {}).get("id")
        items = data.get("purchase", {}).get("virtual_items", {}).get("items", [])

        if not user_id or not items:
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Process each item in the purchase
        for item_data in items:
            sku = item_data.get("sku")
            order_id = f"xsolla_{data.get('notification_type')}_{user_id}_{sku}"

            # Check if this purchase is already confirmed
            if db.query(Purchase).filter(Purchase.order_id == order_id).first():
                continue

            # Look for pending purchase
            pending = (
                db.query(PendingPurchase)
                .filter(
                    PendingPurchase.user_id == user_id, PendingPurchase.item_id == sku
                )
                .first()
            )

            if not pending:
                continue

            # Create confirmed purchase
            purchase = Purchase(user_id=user_id, item_id=sku, order_id=order_id)
            db.add(purchase)
            db.delete(pending)  # Remove pending purchase

        db.commit()

        # Send notification
        notification = {
            "type": "purchase_success",
            "user_id": user_id,
            "items": [
                {"id": item["sku"], "name": db.query(Item).get(item["sku"]).name}
                for item in items
                if db.query(Item).get(item["sku"])
            ],
        }

        for client in connected_clients:
            try:
                await client.send_json(notification)
            except:
                connected_clients.remove(client)

        return {"status": "success"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
