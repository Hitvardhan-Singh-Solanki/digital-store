import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json
from main import app
from models import Item
from database import redis_client

client = TestClient(app)


@pytest.fixture
def db_items(db: Session):
    items = [
        Item(name="Test Item 1", price=10.99, description="Test Description 1"),
        Item(name="Test Item 2", price=20.99, description="Test Description 2"),
    ]
    for item in items:
        db.add(item)
    db.commit()
    yield items
    db.query(Item).delete()
    db.commit()
    redis_client.delete("items")


def test_get_items_without_cache(db: Session, db_items):
    redis_client.delete("items")
    response = client.get("/api/items/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["name"] == "Test Item 1"
    assert items[1]["name"] == "Test Item 2"
    assert "price" in items[0]
    assert "description" in items[0]


def test_get_items_with_cache(db: Session, db_items):
    # First call to populate cache
    client.get("/api/items/")

    # Modify database but don't update cache
    new_item = Item(name="Test Item 3", price=30.99, description="Test Description 3")
    db.add(new_item)
    db.commit()

    # Second call should return cached data
    response = client.get("/api/items/")
    items = response.json()
    assert len(items) == 2  # Should return cached items (2) not including the new item


def test_get_items_empty_db(db: Session):
    redis_client.delete("items")
    response = client.get("/api/items/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 0


def test_create_item(db: Session):
    redis_client.delete("items")
    item_data = {"name": "New Item", "description": "A brand new item", "price": 15.99}

    response = client.post("/api/items/", json=item_data)
    assert response.status_code == 200
    created_item = response.json()
    assert created_item["name"] == item_data["name"]
    assert created_item["description"] == item_data["description"]
    assert created_item["price"] == item_data["price"]
    assert "id" in created_item
