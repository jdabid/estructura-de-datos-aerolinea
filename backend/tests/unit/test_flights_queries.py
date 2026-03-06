from src.features.flights.queries import get_flights, get_destinations, get_flight_by_number
from src.features.flights.commands import create_destination, create_flight
from src.features.flights.schemas import DestinationCreate, FlightCreate


class TestGetFlights:
    def test_get_flights_empty(self, db_session):
        result = get_flights(db_session)
        assert result == []

    def test_get_flights_after_adding(self, db_session):
        destination = create_destination(
            db_session,
            DestinationCreate(name="Cancun", tax_amount=25.0),
        )
        create_flight(
            db_session,
            FlightCreate(
                flight_number="AV123",
                origin="Bogota",
                base_price=200.0,
                destination_id=destination.id,
            ),
        )
        create_flight(
            db_session,
            FlightCreate(
                flight_number="AV456",
                origin="Medellin",
                base_price=180.0,
                destination_id=destination.id,
            ),
        )

        result = get_flights(db_session)
        assert len(result) == 2

    def test_get_flights_returns_correct_data(self, db_session):
        destination = create_destination(
            db_session,
            DestinationCreate(name="Lima", tax_amount=10.0),
        )
        create_flight(
            db_session,
            FlightCreate(
                flight_number="LA789",
                origin="Santiago",
                base_price=300.0,
                destination_id=destination.id,
            ),
        )

        result = get_flights(db_session)
        assert len(result) == 1
        assert result[0].flight_number == "LA789"
        assert result[0].origin == "Santiago"
        assert result[0].base_price == 300.0


class TestGetDestinations:
    def test_get_destinations_empty(self, db_session):
        result = get_destinations(db_session)
        assert result == []

    def test_get_destinations_after_adding(self, db_session):
        create_destination(
            db_session,
            DestinationCreate(name="Cancun", tax_amount=25.0),
        )
        create_destination(
            db_session,
            DestinationCreate(name="Lima", tax_amount=10.0),
        )

        result = get_destinations(db_session)
        assert len(result) == 2

    def test_get_destinations_returns_correct_data(self, db_session):
        create_destination(
            db_session,
            DestinationCreate(name="Madrid", tax_amount=30.0, is_promotion=True),
        )

        result = get_destinations(db_session)
        assert len(result) == 1
        assert result[0].name == "Madrid"
        assert result[0].tax_amount == 30.0
        assert result[0].is_promotion is True


class TestGetFlightByNumber:
    def test_flight_found(self, db_session):
        destination = create_destination(
            db_session,
            DestinationCreate(name="Cancun", tax_amount=25.0),
        )
        create_flight(
            db_session,
            FlightCreate(
                flight_number="AV123",
                origin="Bogota",
                base_price=200.0,
                destination_id=destination.id,
            ),
        )

        result = get_flight_by_number(db_session, "AV123")
        assert result is not None
        assert result.flight_number == "AV123"
        assert result.origin == "Bogota"

    def test_flight_not_found_returns_none(self, db_session):
        result = get_flight_by_number(db_session, "NONEXISTENT")
        assert result is None

    def test_flight_by_number_returns_exact_match(self, db_session):
        destination = create_destination(
            db_session,
            DestinationCreate(name="Lima", tax_amount=10.0),
        )
        create_flight(
            db_session,
            FlightCreate(
                flight_number="AV100",
                origin="Bogota",
                base_price=200.0,
                destination_id=destination.id,
            ),
        )
        create_flight(
            db_session,
            FlightCreate(
                flight_number="AV200",
                origin="Medellin",
                base_price=180.0,
                destination_id=destination.id,
            ),
        )

        result = get_flight_by_number(db_session, "AV200")
        assert result is not None
        assert result.flight_number == "AV200"
        assert result.origin == "Medellin"
