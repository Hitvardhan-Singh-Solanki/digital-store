from sqlalchemy.orm import Session
import sys
import os

# Add the parent directory to the Python path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import SessionLocal
from models import Item


def delete_all_items():
    db = SessionLocal()
    try:
        # Delete all items
        num_deleted = db.query(Item).delete()
        db.commit()
        print(f"Successfully deleted {num_deleted} items!")

    except Exception as e:
        print(f"Error deleting items: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    delete_all_items()
