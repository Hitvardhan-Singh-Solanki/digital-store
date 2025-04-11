from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from simulate_webhook import simulate_webhook
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


class PaymentIntent(BaseModel):
    user_id: str
    item_id: int
    amount: float


@app.post("/register-payment-intent")
def register_payment_intent(intent: PaymentIntent):
    logger.info(f"Received payment intent: {intent}")
    try:
        simulate_webhook(intent.user_id, intent.item_id, intent.amount)
        logger.info("Webhook simulation completed successfully")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to process payment intent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Payment Intent Server is running"}
