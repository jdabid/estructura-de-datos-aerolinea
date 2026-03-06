import sys
from unittest.mock import MagicMock

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


# Replace src.shared.database module with our mock before models are imported.
# This avoids the real database.py trying to connect to PostgreSQL with
# pool_size/max_overflow args that are incompatible with SQLite.
_mock_db_module = type(sys)("src.shared.database")
_mock_db_module.Base = Base
_mock_db_module.get_db = MagicMock()
_mock_db_module.engine = MagicMock()
_mock_db_module.SessionLocal = MagicMock()
sys.modules["src.shared.database"] = _mock_db_module

import pytest  # noqa: E402

# Now import models - they will use our Base instead of the real one.
# Booking model must also be imported because Flight has a relationship to it.
import src.features.flights.models  # noqa: E402, F401
import src.features.bookings.models  # noqa: E402, F401


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
