import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cart():
    client.delete("/cart")
    yield
    client.delete("/cart")


# ── POST /cart/items ─────────────────────────────────────────────────────────

def test_add_item_success():
    response = client.post("/cart/items", json={"menu_id": 1, "quantity": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["menu_id"] == 1
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["subtotal"] == data["items"][0]["price"] * 2
    assert data["total_price"] == data["items"][0]["subtotal"]


def test_add_item_accumulates_quantity():
    client.post("/cart/items", json={"menu_id": 1, "quantity": 1})
    response = client.post("/cart/items", json={"menu_id": 1, "quantity": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["quantity"] == 3


def test_add_sold_out_item_returns_400():
    # Cola (id=4) is is_sold_out=true in sample_menus.json
    response = client.post("/cart/items", json={"menu_id": 4, "quantity": 1})
    assert response.status_code == 400


def test_add_nonexistent_menu_returns_404():
    response = client.post("/cart/items", json={"menu_id": 9999, "quantity": 1})
    assert response.status_code == 404


def test_add_zero_quantity_returns_422():
    response = client.post("/cart/items", json={"menu_id": 1, "quantity": 0})
    assert response.status_code == 422


def test_add_negative_quantity_returns_422():
    response = client.post("/cart/items", json={"menu_id": 1, "quantity": -1})
    assert response.status_code == 422


# ── PUT /cart/items/{menu_id} ────────────────────────────────────────────────

def test_update_item_success():
    client.post("/cart/items", json={"menu_id": 1, "quantity": 1})
    response = client.put("/cart/items/1", json={"quantity": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["quantity"] == 5


def test_update_item_recalculates_total_price():
    client.post("/cart/items", json={"menu_id": 1, "quantity": 1})
    client.post("/cart/items", json={"menu_id": 2, "quantity": 1})
    response = client.put("/cart/items/1", json={"quantity": 3})
    assert response.status_code == 200
    data = response.json()
    item1 = next(i for i in data["items"] if i["menu_id"] == 1)
    item2 = next(i for i in data["items"] if i["menu_id"] == 2)
    assert data["total_price"] == item1["subtotal"] + item2["subtotal"]


def test_update_nonexistent_item_returns_404():
    response = client.put("/cart/items/9999", json={"quantity": 1})
    assert response.status_code == 404


def test_update_zero_quantity_returns_422():
    client.post("/cart/items", json={"menu_id": 1, "quantity": 1})
    response = client.put("/cart/items/1", json={"quantity": 0})
    assert response.status_code == 422


# ── DELETE /cart/items/{menu_id} ─────────────────────────────────────────────

def test_remove_item_success():
    client.post("/cart/items", json={"menu_id": 1, "quantity": 1})
    response = client.delete("/cart/items/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["total_price"] == 0


def test_remove_nonexistent_item_returns_404():
    response = client.delete("/cart/items/9999")
    assert response.status_code == 404


# ── GET /cart ────────────────────────────────────────────────────────────────

def test_get_cart_empty():
    response = client.get("/cart")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total_price"] == 0


def test_get_cart_with_items():
    client.post("/cart/items", json={"menu_id": 1, "quantity": 2})
    client.post("/cart/items", json={"menu_id": 2, "quantity": 1})
    response = client.get("/cart")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total_price"] > 0


# ── DELETE /cart ─────────────────────────────────────────────────────────────

def test_clear_cart():
    client.post("/cart/items", json={"menu_id": 1, "quantity": 1})
    response = client.delete("/cart")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total_price"] == 0
