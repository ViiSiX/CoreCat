import pytest
import datetime


@pytest.fixture
def freeze_datetime(monkeypatch):
    """Patch datetime.now function to return fixed timestamp."""
    original_datetime = datetime.datetime

    class FrozenDateTimeMeta(type):
        """Meta class for FrozenDateTime class."""
        def __instancecheck__(self, instance):
            return isinstance(instance, (original_datetime, FrozenDateTime))

    class FrozenDateTime(datetime.datetime):
        """Use freeze method to control result of datetime.datetime.now()."""
        __metaclass__ = FrozenDateTimeMeta

        @classmethod
        def freeze(cls, freezing_timestamp):
            """Freeze time at freezing_timestamp."""
            cls.frozen_time = freezing_timestamp

        @classmethod
        def now(cls, tz=None):
            """Return the frozen time."""
            return cls.frozen_time

    monkeypatch.setattr(datetime, 'datetime', FrozenDateTime)
    FrozenDateTime.freeze(original_datetime.now())
    return FrozenDateTime
