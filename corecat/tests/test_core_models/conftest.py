"""Setup and initialization for Models' Unit Tests."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from corecat.models.user import User
from corecat.models.groups import Group
from corecat.models.directory import Directory
from corecat.models.project import Project
from corecat.models.source import SourceBase, SourceAttribute
from corecat.tests._utils import freeze_datetime


@pytest.fixture
def fix_create_all_tables():
    """Create all the table into an in-memory SQLite database."""

    engine = create_engine('sqlite://')

    # Create tables
    # TODO: Auto create all
    User.__table__.create(engine, checkfirst=True)
    Group.__table__.create(engine, checkfirst=True)
    Project.__table__.create(engine, checkfirst=True)
    Directory.__table__.create(engine, checkfirst=True)
    SourceBase.__table__.create(engine, checkfirst=True)
    SourceAttribute.__table__.create(engine, checkfirst=True)

    session = sessionmaker(bind=engine)
    session = session()

    return session


@pytest.fixture
def fix_add_user(fix_create_all_tables):
    """Add an user to in-memory database."""

    session = fix_create_all_tables
    user = User(
        user_email=None,
        user_password='Hey! Jim!',
        user_name='root',
        user_id=0
    )
    session.add(user)
    session.commit()

    return session, user
