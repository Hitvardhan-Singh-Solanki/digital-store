import httpx
import logging
from database import SessionLocal
from models import PendingPurchase

logger = logging.getLogger(__name__)


async def delete_pending_purchase(order_id: str):
    """
    Deletes a PendingPurchase record by order_id from the database.

    Args:
        order_id (str): The unique order_id of the PendingPurchase to delete.

    Returns:
        bool: True if the record was found and deleted, False if not found.

    Raises:
        Exception: If a database error occurs during deletion.
    """
    try:
        db = SessionLocal()
        try:
            pending_purchase = (
                db.query(PendingPurchase)
                .filter(PendingPurchase.order_id == order_id)
                .first()
            )
            if pending_purchase:
                db.delete(pending_purchase)
                db.commit()
                logger.info(f"Deleted pending purchase for order {order_id}")
                return True
            else:
                logger.warning(
                    f"No pending purchase found for order {order_id} to delete"
                )
                return False
        finally:
            db.close()
    except Exception as db_error:
        logger.error(
            f"Failed to delete pending purchase for order {order_id}: {db_error}"
        )
        raise


async def send_payment_intent(user_id: str, item_id: int, order_id: str, amount: float):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://webhook-simulator:8001/register-payment-intent",
                json={
                    "user_id": user_id,
                    "item_id": item_id,
                    "amount": amount,
                },
                timeout=5,
            )
            response.raise_for_status()
            logger.info(
                f"Payment intent sent successfully for order {order_id}: {response.json()}"
            )
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        logger.error(f"Payment intent failed for order {order_id}: {e}")
        try:
            await delete_pending_purchase(order_id)
        except Exception as db_error:
            logger.error(
                f"Deletion attempt failed for order {order_id} after payment intent error: {db_error}"
            )
    except Exception as e:
        logger.error(f"Unexpected error in payment intent for order {order_id}: {e}")
        try:
            await delete_pending_purchase(order_id)
        except Exception as db_error:
            logger.error(
                f"Deletion attempt failed for order {order_id} after unexpected error: {db_error}"
            )
