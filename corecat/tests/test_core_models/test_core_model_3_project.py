import datetime
from corecat.models.project import Project
from corecat.constants import OBJECT_CODES, MODEL_VERSION


class TestProjectModel(object):
    """Unit tests for Project model."""

    project_1 = {
        'project_name': 'Project #1',
        'project_description': 'Description for Project #1',
        'created_by_user_id': 0,
    }

    project_2 = {
        'project_name': 'Project #2',
        'project_description': 'Description for Project #2',
        'created_by_user_id': 0,
    }

    def test_would_init_work(self, fix_add_user):
        """Check if class initial logic is working or not."""

        project = Project(**self.project_1)

        assert project.project_name
        assert project.project_description
        assert project._version == MODEL_VERSION[OBJECT_CODES['Project']]

    def test_would_default_value_worked(self,
                                        fix_create_all_tables
                                        ):
        """Confirm again the default values after insert into Database."""

        session = fix_create_all_tables

        project_1 = Project(**self.project_1)
        session.add(project_1)
        session.commit()

        assert project_1.project_id == 1
        assert project_1.is_active
        assert not project_1.is_deleted
        assert project_1.created_by == 0
        assert project_1.last_updated_by == 0
        datetime_now = datetime.datetime.now()
        assert round(
            (datetime_now - project_1.created_on).total_seconds()
        ) == 0
        assert round(
            (datetime_now - project_1.last_updated_on).total_seconds()
        ) == 0

        project_2 = Project(**self.project_2)
        session.add(project_2)
        session.commit()

        assert project_2.project_id == 2
        assert project_2.created_by == 0
        assert project_2.last_updated_by == 0
