import datetime
from corecat.models.directory import Directory
from corecat.constants import OBJECT_CODES, MODEL_VERSION


class TestProjectModel(object):
    """Unit tests for Project model."""

    directory_1 = {
        'directory_name': 'directory #1',
        'directory_description': 'Description for directory #1',
        'created_by_user_id': 1,
    }

    directory_2 = {
        'directory_name': 'directory #2',
        'directory_description': 'Description for directory #2',
        'created_by_user_id': 1,
    }

    def test_would_init_work(self, fix_add_user):
        """Check if class initial logic is working or not."""

        directory = Directory(**self.directory_1)

        assert directory.directory_name
        assert directory.directory_description
        assert directory._version == MODEL_VERSION[OBJECT_CODES['Directory']]

    def test_would_default_value_worked(self,
                                        fix_create_all_tables
                                        ):
        """Confirm again the default values after insert into Database."""

        session = fix_create_all_tables

        directory_1 = Directory(**self.directory_1)
        session.add(directory_1)
        session.commit()

        assert directory_1.is_active
        assert not directory_1.is_deleted
        assert directory_1.created_by == 1
        assert directory_1.last_updated_by == 1
        datetime_now = datetime.datetime.now()
        assert round(
            (datetime_now - directory_1.created_on).total_seconds()
        ) == 0
        assert round(
            (datetime_now - directory_1.last_updated_on).total_seconds()
        ) == 0

        directory_2 = Directory(**self.directory_2)
        session.add(directory_2)
        session.commit()

        assert directory_2.created_by == 1
        assert directory_2.last_updated_by == 1
