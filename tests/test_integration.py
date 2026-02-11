import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.shared.database import Base, engine

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_full_booking_flow():
    dest_resp = client.post("/api/v1/flights/destinations/", json={
        "name": "Cartagena",
        "tax_amount": 50.0,
        "is_promotion": True,
        "allows_pets": True,
    })
    assert dest_resp.status_code == 200
    dest_id = dest_resp.json()["id"]

    flight_resp = client.post("/api/v1/flights/", json={
        "flight_number": "CT-123",
        "origin": "Bogota",
        "base_price": 1000.0,
        "destination_id": dest_id,
    })
    assert flight_resp.status_code == 200
    flight_id = flight_resp.json()["id"]

    booking_resp = client.post("/api/v1/bookings/", json={
        "passenger_name": "Juan Perez",
        "passenger_age": 30,
        "has_pet": True,
        "flight_id": flight_id,
    })
    assert booking_resp.status_code == 200
    assert booking_resp.json()["total_price"] == 950.0


def test_pet_validation_error():
    dest_resp = client.post("/api/v1/flights/destinations/", json={
        "name": "Londres",
        "tax_amount": 100,
        "is_promotion": False,
        "allows_pets": False,
    })
    assert dest_resp.status_code == 200
    dest_id = dest_resp.json()["id"]

    flight_resp = client.post("/api/v1/flights/", json={
        "flight_number": "LON-99",
        "origin": "Bogota",
        "base_price": 2000,
        "destination_id": dest_id,
    })
    assert flight_resp.status_code == 200
    flight_id = flight_resp.json()["id"]

    resp = client.post("/api/v1/bookings/", json={
        "passenger_name": "Mascota Lover",
        "passenger_age": 25,
        "has_pet": True,
        "flight_id": flight_id,
    })
    assert resp.status_code == 400
    assert "no acepta mascotas" in resp.json()["detail"]


def test_negative_price_rejected():
    dest_resp = client.post("/api/v1/flights/destinations/", json={
        "name": "Test City",
        "tax_amount": 10.0,
    })
    dest_id = dest_resp.json()["id"]

    resp = client.post("/api/v1/flights/", json={
        "flight_number": "NEG-01",
        "origin": "Bogota",
        "base_price": -100,
        "destination_id": dest_id,
    })
    assert resp.status_code == 422


def test_invalid_age_rejected():
    resp = client.post("/api/v1/bookings/", json={
        "passenger_name": "Ghost",
        "passenger_age": -5,
        "flight_id": 999,
    })
    assert resp.status_code == 422
