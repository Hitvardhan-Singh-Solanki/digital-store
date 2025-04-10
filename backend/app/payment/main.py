import requests
import logging

logger = logging.getLogger(__name__)


def send_payment_intent(user_id: str, item_id: int):
    try:
        response = requests.post(
            "http://webhook-simulator:8001/register-payment-intent",
            json={"user_id": user_id, "item_id": item_id},
            timeout=5,
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Async payment intent failed: {e}")
