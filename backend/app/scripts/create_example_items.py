from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import SessionLocal
from models import Item


def create_example_items():
    db = SessionLocal()
    try:
        # Create example game items
        items = [
            Item(
                name="Dragon Sword",
                description="A legendary sword with dragon-slaying powers",
                price=999.99,
            ),
            Item(
                name="Magic Shield",
                description="An enchanted shield that blocks magical attacks",
                price=499.99,
            ),
            Item(
                name="Speed Boots",
                description="Boots that increase your movement speed by 50%",
                price=299.99,
            ),
            Item(
                name="Health Potion",
                description="Restores 100 HP instantly",
                price=49.99,
            ),
            Item(
                name="Wizard Hat",
                description="Increases magic power by 25%",
                price=199.99,
            ),
        ]

        # Add all items to the database
        for item in items:
            db.add(item)

        db.commit()
        print("Successfully created example items!")

    except Exception as e:
        print(f"Error creating items: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_example_items()
