import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_full_booking_flow():
    # 1. Crear un destino con promoción e impuestos
    dest_resp = client.post("/api/v1/flights/destinations/", json={
        "name": "Cartagena",
        "tax_amount": 50.0,
        "is_promotion": True,
        "allows_pets": True
    })
    assert dest_resp.status_code == 200
    dest_id = dest_resp.json()["id"]

    # 2. Crear un vuelo para ese destino
    flight_resp = client.post("/api/v1/flights/", json={
        "flight_number": "CT-123",
        "origin": "Bogotá",
        "base_price": 1000.0,
        "destination_id": dest_id
    })
    assert flight_resp.status_code == 200
    flight_id = flight_resp.json()["id"]

    # 3. Realizar una reserva (Debería aplicar 10% desc + 50 de impuesto)
    # 1000 * 0.9 = 900 + 50 = 950
    booking_resp = client.post("/api/v1/bookings/", json={
        "passenger_name": "Juan Perez",
        "passenger_age": 30,
        "has_pet": True,
        "flight_id": flight_id
    })
    assert booking_resp.status_code == 200
    assert booking_resp.json()["total_price"] == 950.0


def test_pet_validation_error():
    # Intentar reservar con mascota en destino que no permite
    client.post("/api/v1/flights/destinations/", json={
        "name": "Londres", "tax_amount": 100, "allows_pets": False
    })
    # ... asumiendo que el ID es 2
    client.post("/api/v1/flights/", json={
        "flight_number": "LON-99", "origin": "Bog", "base_price": 2000, "destination_id": 2
    })

    resp = client.post("/api/v1/bookings/", json={
        "passenger_name": "Mascota Lover", "passenger_age": 25, "has_pet": True, "flight_id": 2
    })
    assert resp.status_code == 400
    assert "no acepta mascotas" in resp.json()["detail"]