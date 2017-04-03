import datetime
from corecat.models.source import SourceBase, SourceAttribute
from corecat.constants import OBJECT_CODES, MODEL_VERSION, \
    SOURCE_TYPE_CODES


class TestSourceModel(object):
    """Unit tests for Project model."""

    source_1 = {
        'source_name': 'Data Source #1',
        'created_by_user_id': 0,
        'source_type': SOURCE_TYPE_CODES['Base']
    }

    source_2 = {
        'source_name': 'Data Source #1',
        'created_by_user_id': 0,
        'source_type': SOURCE_TYPE_CODES['Base']
    }

    def test_would_init_work(self, fix_add_user):
        """Check if class initial logic is working or not."""

        source = SourceBase(**self.source_1)

        assert source.source_name
        assert source.source_type is not None
        assert isinstance(source.source_type, int)
        assert source._version == MODEL_VERSION[OBJECT_CODES['Source']]

    def test_would_default_value_worked(self,
                                        fix_create_all_tables
                                        ):
        """Confirm again the default values after insert into Database."""

        session = fix_create_all_tables

        source_1 = SourceBase(**self.source_1)
        session.add(source_1)
        session.commit()

        assert source_1.source_id == 1
        assert source_1.is_active
        assert not source_1.is_deleted
        assert source_1.created_by == 0
        assert source_1.last_updated_by == 0
        datetime_now = datetime.datetime.now()
        assert round(
            (datetime_now - source_1.created_on).total_seconds()
        ) == 0
        assert round(
            (datetime_now - source_1.last_updated_on).total_seconds()
        ) == 0

        source_2 = SourceBase(**self.source_2)
        session.add(source_2)
        session.commit()

        assert source_2.source_id == 2
        assert source_2.created_by == 0
        assert source_2.last_updated_by == 0

    def test_would_add_custom_attribute_success(self, fix_create_all_tables):
        """Add Custom attribute to a Data Source."""

        session = fix_create_all_tables

        source = SourceBase(**self.source_1)
        session.add(source)
        session.commit()

        base_uri = 'file:///some/file/here'
        source['base_uri'] = base_uri
        session.commit()

        source_get = session.query(SourceBase).\
            filter_by(source_id=source.source_id).first()
        assert source_get.source_id == 1
        assert source_get['base_uri'] == base_uri

        attribute_get = session.query(SourceAttribute).first()
        assert attribute_get.source_id == source_get.source_id
        assert attribute_get.attribute_name == 'base_uri'
        assert attribute_get.attribute_value == base_uri
