import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json
import hmac
import hashlib
from main import app
from models import Item, Purchase, User

client = TestClient(app)


def create_signature(payload: dict, secret: str = "somesecret") -> str:
    body = json.dumps(payload)
    return hmac.new(secret.encode(), body.encode(), hashlib.sha1).hexdigest()


@pytest.fixture
def test_data(db: Session):
    # Create test user and item
    user = User(id="user123", username="testuser", password="hashed_password")
    item = Item(id=1, name="Test Item", price=9.99, description="Test Description")
    db.add(user)
    db.add(item)
    db.commit()

    yield {"user": user, "item": item}

    db.query(Purchase).delete()
    db.query(User).delete()
    db.query(Item).delete()
    db.commit()


def test_webhook_valid_signature(test_data):
    payload = {
        "notification_type": "payment",
        "user": {"id": "user123"},
        "purchase": {"virtual_items": {"items": [{"sku": "1", "amount": 1}]}},
    }

    signature = create_signature(payload)
    response = client.post(
        "/api/webhooks/payment",
        json=payload,
        headers={"Authorization": f"Signature {signature}"},
    )

    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_webhook_invalid_signature(test_data):
    payload = {
        "notification_type": "payment",
        "user": {"id": "user123"},
        "purchase": {"virtual_items": {"items": [{"sku": "1", "amount": 1}]}},
    }

    response = client.post(
        "/api/webhooks/payment",
        json=payload,
        headers={"Authorization": "Signature invalid"},
    )

    assert response.status_code == 401


def test_webhook_duplicate_order(test_data, db: Session):
    # Create a purchase first
    purchase = Purchase(
        user_id="user123", item_id=1, order_id="xsolla_payment_user123_1"
    )
    db.add(purchase)
    db.commit()

    # Try to create the same purchase via webhook
    payload = {
        "notification_type": "payment",
        "user": {"id": "user123"},
        "purchase": {"virtual_items": {"items": [{"sku": "1", "amount": 1}]}},
    }

    signature = create_signature(payload)
    response = client.post(
        "/api/webhooks/payment",
        json=payload,
        headers={"Authorization": f"Signature {signature}"},
    )

    assert response.status_code == 200
    # Verify no duplicate purchase was created
    purchases = (
        db.query(Purchase).filter_by(order_id="xsolla_payment_user123_1").count()
    )
    assert purchases == 1
