import requests
import hmac
import hashlib
import json
import os
from time import sleep


def simulate_webhook(user_id, item_id):
    # Webhook payload
    payload = {
        "notification_type": "payment",
        "user": {"id": user_id},
        "purchase": {
            "virtual_items": {
                "items": [
                    {
                        "sku": item_id,
                        "amount": 1,
                    }
                ]
            }
        },
    }

    # Convert payload to JSON string
    body = json.dumps(payload).encode()

    # Calculate signature
    secret = os.getenv("XSOLLA_WEBHOOK_SECRET", "supersecret")
    signature = hmac.new(secret.encode(), body, hashlib.sha1).hexdigest()

    # Send webhook request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Signature {signature}",
    }

    # Use backend service name instead of localhost
    response = requests.post(
        "http://backend:8000/api/webhooks/payment", data=body, headers=headers
    )

    print(f"Webhook response: {response.status_code}")
    print(response.json())


if __name__ == "__main__":
    print("Starting webhook simulator...")
    while True:
        try:
            simulate_webhook("0a948c0e-b786-423c-915e-c21a29539dc6", "6")
        except Exception as e:
            print(f"Error sending webhook: {e}")
        sleep(3)
