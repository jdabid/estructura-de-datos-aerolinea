import pytest
from pydantic import ValidationError
from src.features.flights.commands import create_destination, create_flight
from src.features.flights.schemas import DestinationCreate, FlightCreate
from src.features.flights.models import Destination, Flight


class TestCreateDestination:
    def test_create_destination_successfully(self, db_session):
        destination_data = DestinationCreate(
            name="Cancun",
            tax_amount=25.0,
            is_promotion=True,
            allows_pets=False,
        )
        result = create_destination(db_session, destination_data)

        assert result.id is not None
        assert result.name == "Cancun"
        assert result.tax_amount == 25.0
        assert result.is_promotion is True
        assert result.allows_pets is False

    def test_create_destination_with_defaults(self, db_session):
        destination_data = DestinationCreate(
            name="Bogota",
            tax_amount=10.0,
        )
        result = create_destination(db_session, destination_data)

        assert result.name == "Bogota"
        assert result.is_promotion is False
        assert result.allows_pets is True

    def test_create_destination_with_zero_tax(self, db_session):
        destination_data = DestinationCreate(
            name="Lima",
            tax_amount=0.0,
        )
        result = create_destination(db_session, destination_data)

        assert result.tax_amount == 0.0

    def test_create_destination_persists_in_db(self, db_session):
        destination_data = DestinationCreate(
            name="Madrid",
            tax_amount=15.0,
        )
        create_destination(db_session, destination_data)

        db_result = db_session.query(Destination).filter_by(name="Madrid").first()
        assert db_result is not None
        assert db_result.tax_amount == 15.0


class TestCreateFlight:
    def test_create_flight_successfully(self, db_session):
        destination_data = DestinationCreate(
            name="Cancun",
            tax_amount=25.0,
        )
        destination = create_destination(db_session, destination_data)

        flight_data = FlightCreate(
            flight_number="AV123",
            origin="Bogota",
            base_price=200.0,
            destination_id=destination.id,
        )
        result = create_flight(db_session, flight_data)

        assert result.id is not None
        assert result.flight_number == "AV123"
        assert result.origin == "Bogota"
        assert result.base_price == 200.0
        assert result.destination_id == destination.id

    def test_create_flight_persists_in_db(self, db_session):
        destination_data = DestinationCreate(
            name="Lima",
            tax_amount=10.0,
        )
        destination = create_destination(db_session, destination_data)

        flight_data = FlightCreate(
            flight_number="LA456",
            origin="Santiago",
            base_price=350.0,
            destination_id=destination.id,
        )
        create_flight(db_session, flight_data)

        db_result = db_session.query(Flight).filter_by(flight_number="LA456").first()
        assert db_result is not None
        assert db_result.origin == "Santiago"
        assert db_result.base_price == 350.0


class TestDestinationSchemaValidation:
    def test_negative_tax_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            DestinationCreate(
                name="Cancun",
                tax_amount=-5.0,
            )
        assert "tax_amount no puede ser negativo" in str(exc_info.value)

    def test_zero_tax_is_valid(self):
        destination = DestinationCreate(
            name="Cancun",
            tax_amount=0.0,
        )
        assert destination.tax_amount == 0.0


class TestFlightSchemaValidation:
    def test_zero_price_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            FlightCreate(
                flight_number="AV123",
                origin="Bogota",
                base_price=0.0,
                destination_id=1,
            )
        assert "base_price debe ser mayor a 0" in str(exc_info.value)

    def test_negative_price_raises_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            FlightCreate(
                flight_number="AV123",
                origin="Bogota",
                base_price=-100.0,
                destination_id=1,
            )
        assert "base_price debe ser mayor a 0" in str(exc_info.value)

    def test_positive_price_is_valid(self):
        flight = FlightCreate(
            flight_number="AV123",
            origin="Bogota",
            base_price=150.0,
            destination_id=1,
        )
        assert flight.base_price == 150.0
