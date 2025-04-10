import requests
import hmac
import hashlib
import json
import os
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def simulate_webhook(user_id: str, item_id: int):
    logger.info(f"Starting webhook simulation for user {user_id}, item {item_id}")
    payload = {
        "notification_type": "payment",
        "user": {"id": user_id},
        "purchase": {
            "virtual_items": {
                "items": [
                    {
                        "sku": str(item_id),
                        "amount": 1,
                    }
                ]
            }
        },
    }

    body = json.dumps(payload).encode()

    secret = os.getenv("XSOLLA_WEBHOOK_SECRET")
    signature = hmac.new(secret.encode(), body, hashlib.sha1).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Signature {signature}",
    }

    logger.debug(f"Sending webhook request with payload: {payload}")

    try:
        sleep(3)  # to simulate some work load like card details etc
        response = requests.post(
            "http://backend:8000/api/webhooks/payment",
            json=payload,
            headers=headers,
            timeout=5,
        )
        logger.info(f"Webhook response: {response.status_code}")
        response.raise_for_status()
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Webhook simulation failed: {e}")
        raise
