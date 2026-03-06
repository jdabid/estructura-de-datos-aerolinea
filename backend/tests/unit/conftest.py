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

# Mock redis client module
_mock_redis = type(sys)("src.shared.redis_client")
_mock_redis.update_stat = MagicMock()
_mock_redis.log_to_list = MagicMock()
sys.modules["src.shared.redis_client"] = _mock_redis

# Mock celery app module
_mock_celery_app = type(sys)("src.worker.celery_app")
_mock_celery_app.celery_app = MagicMock()
sys.modules["src.worker.celery_app"] = _mock_celery_app

# Mock worker tasks module
_mock_tasks = type(sys)("src.worker.tasks")
_mock_tasks.process_booking_event = MagicMock()
sys.modules["src.worker.tasks"] = _mock_tasks

import pytest  # noqa: E402

# Now import models - they will use our Base instead of the real one.
import src.features.flights.models  # noqa: E402, F401
import src.features.bookings.models  # noqa: E402, F401
import src.features.auth.models  # noqa: E402, F401


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
