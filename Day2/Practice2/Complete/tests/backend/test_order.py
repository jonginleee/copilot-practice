from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.db.models import Order, OrderItem
from app.db.session import SessionLocal
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_state() -> None:
    client.delete("/cart")
    db = SessionLocal()
    try:
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_order_success_and_persisted(db_session) -> None:
    client.post("/cart/items", json={"menu_id": 1, "quantity": 2})

    response = client.post("/orders")
    assert response.status_code == 200
    payload = response.json()

    assert isinstance(payload["order_number"], int)
    assert payload["order_number"] >= 1
    # Validate timestamp format: YYYY-MM-DD HH:MM:SS
    datetime.strptime(payload["timestamp"], "%Y-%m-%d %H:%M:%S")
    assert payload["total_price"] > 0
    assert len(payload["items"]) == 1
    assert payload["items"][0]["category"] == "burger"
    assert payload["items"][0]["image_url"]

    db_order = db_session.query(Order).filter_by(id=payload["order_number"]).first()
    assert db_order is not None
    assert db_order.total_price == payload["total_price"]

    db_items = db_session.query(OrderItem).filter_by(order_id=payload["order_number"]).all()
    assert len(db_items) == 1
    assert db_items[0].category == payload["items"][0]["category"]
    assert db_items[0].image_url == payload["items"][0]["image_url"]

    cart_response = client.get("/cart")
    assert cart_response.status_code == 200
    assert cart_response.json()["items"] == []


def test_create_order_empty_cart_returns_400() -> None:
    response = client.post("/orders")
    assert response.status_code == 400
