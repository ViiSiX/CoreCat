"""Setup and initialization for Models' Unit Tests."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from corecat.models.user import User


@pytest.fixture
def fix_test_create_user_table():
    engine = create_engine('sqlite://')

    User.__table__.create(bind=engine)

    session = sessionmaker(bind=engine)

    return session()
