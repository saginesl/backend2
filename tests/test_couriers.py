import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_courier():
    courier_data = {
        "name": "petrov",
        "districts": ["october"]
    }
    response = client.post("/couriers/courier", json=courier_data)
    assert response.status_code == 201



def test_list_all_couriers():
    response = client.get("/couriers/couriers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_courier_by_id():
    response = client.get("/couriers/courier/1")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "name" in response.json()


def test_get_courier_by_nonexistent_id():
    response = client.get("/couriers/courier/999")
    assert response.status_code == 404
    assert response.json()["message"] == "courier not found"