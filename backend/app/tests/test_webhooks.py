import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import os
import hmac
import hashlib
import json
from main import app
from models import Purchase

client = TestClient(app)


def test_webhook_invalid_signature(db: Session):
    payload = {
        "notification_type": "test_order_123",
        "user": {"id": 1},
        "purchase": {"virtual_item": {"sku": 1}},
    }

    response = client.post(
        "/api/webhooks/payment",
        json=payload,
        headers={"Authorization": "Signature invalid"},
    )
    assert response.status_code == 401


def test_webhook_valid_signature(db: Session):
    payload = {
        "notification_type": "test_order_123",
        "user": {"id": 1},
        "purchase": {"virtual_item": {"sku": 1}},
    }
    body = json.dumps(payload).encode()
    secret = "supersecret".encode()
    signature = hmac.new(secret, body, hashlib.sha1).hexdigest()

    response = client.post(
        "/api/webhooks/payment",
        json=payload,
        headers={"Authorization": f"Signature {signature}"},
    )
    assert response.status_code == 200

    # Verify purchase was created
    purchase = db.query(Purchase).filter_by(order_id="test_order_123").first()
    assert purchase is not None
    assert purchase.user_id == 1
    assert purchase.item_id == 1


def test_webhook_duplicate_order(db: Session):
    # First purchase
    payload = {
        "notification_type": "duplicate_order_123",
        "user": {"id": 1},
        "purchase": {"virtual_item": {"sku": 1}},
    }
    body = json.dumps(payload).encode()
    secret = "supersecret".encode()
    signature = hmac.new(secret, body, hashlib.sha1).hexdigest()

    client.post(
        "/api/webhooks/payment",
        json=payload,
        headers={"Authorization": f"Signature {signature}"},
    )

    # Duplicate purchase attempt
    response = client.post(
        "/api/webhooks/payment",
        json=payload,
        headers={"Authorization": f"Signature {signature}"},
    )
    assert response.status_code == 409
