import hmac
import hashlib
import requests
import json
import os

url = "http://backend:8000/api/webhooks/payment"
secret = os.getenv("XSOLLA_WEBHOOK_SECRET", "supersecret")

payload = {
    "notification_type": "payment",
    "purchase": {
        "virtual_items": {
            "items": [
                {"sku": "cool_skin", "amount": 1}
            ]
        }
    },
    "user": {"id": "user123"},
    "payment_details": {"amount": "100"}
}

body = json.dumps(payload)
signature = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "Authorization": signature
}

response = requests.post(url, headers=headers, data=body)
print(f"Status: {response.status_code}, Body: {response.text}")