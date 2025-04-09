import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import Purchase, Item
from main import app

client = TestClient(app)


@pytest.fixture
def test_item(db: Session):
    item = Item(name="Test Item", price=10.99, description="Test Description")
    db.add(item)
    db.commit()
    yield item
    db.query(Item).delete()
    db.commit()


@pytest.fixture
def db_purchases(db: Session, test_item):
    purchases = [
        Purchase(user_id=1, item_id=test_item.id, order_id="order1"),
        Purchase(user_id=1, item_id=test_item.id, order_id="order2"),
    ]
    for purchase in purchases:
        db.add(purchase)
    db.commit()
    yield purchases
    db.query(Purchase).delete()
    db.commit()


def test_get_purchases_empty(db: Session):
    response = client.get("/api/purchases/")
    assert response.status_code == 200
    purchases = response.json()
    assert len(purchases) == 0


# def test_get_purchases(db: Session, db_purchases):
#     response = client.get("/api/purchases/")
#     assert response.status_code == 200
#     purchases = response.json()
#     assert len(purchases) == 2
#     assert purchases[0]["order_id"] == "order1"
#     assert purchases[1]["order_id"] == "order2"
#     assert "timestamp" in purchases[0]
#     assert "user_id" in purchases[0]
#     assert "item_id" in purchases[0]
