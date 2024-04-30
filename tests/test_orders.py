import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_order():
    order_data = {
        "name": "newdelivery",
        "district": "october"
    }
    response = client.post("/orders/order", json=order_data)
    assert response.status_code == 201
    assert "order_id" in response.json()
    assert "courier_id" in response.json()


def test_get_order_by_id():
    response = client.get("/orders/order/1")
    assert response.status_code == 200
    assert "courier_id" in response.json()
    assert "status" in response.json()


def test_get_order_by_nonexistent_id():
    response = client.get("/orders/order/999")
    assert response.status_code == 404
    assert response.json()["message"] == "Order not found"


def test_complete_order():
    response = client.post("/orders/order/1")
    assert response.status_code == 201
    assert response.json()["message"] == "Order completed"


def test_complete_nonexistent_order():
    response = client.post("/orders/order/999")
    assert response.status_code == 404
    assert response.json()["message"] == "Order not found"


def test_complete_already_completed_order():
    #если существующий заказ уже завершен
    response = client.post("/orders/order/1")
    assert response.status_code == 201
    assert response.json()["message"] == "Order completed"