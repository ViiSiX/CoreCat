import datetime
import pytest
from sqlalchemy.exc import IntegrityError
from corecat.models.groups import Group
from corecat.constants import OBJECT_CODES, MODEL_VERSION


class TestGroupModel(object):
    """Unit tests for Group model."""

    group_0 = {
        'group_name': 'global group 1',
        'created_by_user_id': 0
    }

    group_1 = {
        'group_name': 'group 1',
        'directory_id': 1,
        'created_by_user_id': 0
    }

    group_2 = {
        'group_name': 'group 2',
        'directory_id': 1,
        'created_by_user_id': 0
    }

    def test_would_init_work(self, fix_add_user):
        """Check if class initial logic is working or not."""

        group = Group(**self.group_1)

        assert group.group_name
        assert group._version == MODEL_VERSION[OBJECT_CODES['Group']]

    def test_would_default_value_worked(self,
                                        fix_create_all_tables
                                        ):
        """Confirm again the default values after insert into Database."""

        session = fix_create_all_tables

        group_1 = Group(**self.group_1)
        session.add(group_1)
        session.commit()

        assert group_1.group_id == 1
        assert group_1.is_active
        assert not group_1.is_deleted
        assert group_1.created_by == 0
        assert group_1.last_updated_by == 0
        datetime_now = datetime.datetime.now()
        assert round(
            (datetime_now - group_1.created_on).total_seconds()
        ) == 0
        assert round(
            (datetime_now - group_1.last_updated_on).total_seconds()
        ) == 0

        group_2 = Group(**self.group_2)
        session.add(group_2)
        session.commit()

        assert group_2.group_id == 2
        assert group_2.created_by == 0
        assert group_2.last_updated_by == 0

    def test_insert_global_group(self, fix_create_all_tables):
        """Insert Global group into the database."""

        session = fix_create_all_tables

        group_0 = Group(**self.group_0)
        session.add(group_0)
        session.commit()

    def test_group_directory_unique_constraint(self, fix_create_all_tables):
        """Group name must be unique in one directory."""

        session = fix_create_all_tables

        session.add(Group(**self.group_1))
        session.commit()
        with pytest.raises(IntegrityError):
            session.add(Group(**self.group_1))
            session.commit()
