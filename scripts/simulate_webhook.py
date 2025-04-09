import hmac
import hashlib
import requests
import json
import os
import uuid


def generate_signature(payload: dict, secret: str) -> str:
    body = json.dumps(payload)
    return hmac.new(secret.encode(), body.encode(), hashlib.sha1).hexdigest()


def send_webhook(url: str, payload: dict, secret: str) -> None:
    # Generate signature
    body = json.dumps(payload)
    signature = generate_signature(payload, secret)

    # Prepare headers with signature
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Signature {signature}",
    }

    # Send request
    response = requests.post(url, headers=headers, data=body)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    # Configuration
    webhook_url = "http://localhost:8000/api/webhooks/payment"
    webhook_secret = os.getenv("XSOLLA_WEBHOOK_SECRET", "supersecret")

    # Example Xsolla webhook payload
    payload = {
        "notification_type": "payment",
        "user": {"id": "user123", "name": {"value": "John Doe"}},
        "purchase": {
            "virtual_items": {
                "items": [
                    {
                        "sku": "1",  # Must match an existing item ID in your database
                        "amount": 1,
                    }
                ]
            }
        },
        "transaction": {
            "id": str(uuid.uuid4()),
            "payment_date": "2024-02-20T12:00:00Z",
        },
        "payment_details": {
            "payment_method": "credit_card",
            "amount": "9.99",
            "currency": "USD",
        },
    }

    send_webhook(webhook_url, payload, webhook_secret)
