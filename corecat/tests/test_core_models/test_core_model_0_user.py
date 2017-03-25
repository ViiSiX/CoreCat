import datetime
import pytest
from sqlalchemy.exc import IntegrityError, \
    InvalidRequestError
from corecat.models.user import User
from corecat.constants import OBJECT_CODES, MODEL_VERSION
from corecat import utils


class TestUserModel(object):
    """Unit tests for User model."""

    user_1 = {
        'user_email': 'test@test.test',
        'user_password': 'YouShallNotPass'
    }
    user_2 = {
        'user_email': 'cat@ta.lina',
        'user_password': 'Candy, Sugar, Salt!'
    }

    def test_would_init_work(self):
        """Check if class initial logic is working or not."""

        user = User(**self.user_1)

        assert user.user_email == self.user_1['user_email']
        assert user.password
        assert utils.check_password(
            user.password, self.user_1['user_password']
        )
        assert user._version == \
            MODEL_VERSION[OBJECT_CODES['User']]

    def test_would_init_fail_on_user_email(self):
        """Check if class initial will be failed on bad email address."""

        with pytest.raises(ValueError) as except_info:
            user = User(
                'mail_ops', 'password'
            )
        assert 'Email mail_ops is not valid!' in str(except_info)

    def test_would_init_fail_on_user_password(self):
        """Check if class initial will be failed on bad password."""

        with pytest.raises(TypeError) as exec_info:
            user = User(
                'mail_ok@mail.mail', None
            )
        assert 'Password should be a string!' in str(exec_info)

    def test_would_get_id_return_an_empty_string(self):
        """Return empty string if ID is None/NULL."""

        user = User(**self.user_1)

        assert user.get_id() == ''

    def test_would_get_id_after_add_user(self, fix_create_all_tables):
        """Make sure ID consequence work."""

        session = fix_create_all_tables

        user_1 = User(**self.user_1)
        session.add(user_1)
        session.commit()
        assert user_1.user_id == 1
        assert user_1.get_id() == "1"
        assert str(user_1) == '<Corecat.User {email} - Id {id}>'.format(
            email=self.user_1['user_email'],
            id=1
        )

        user_2 = User(**self.user_2)
        session.add(user_2)
        session.commit()
        assert user_2.user_id == 2

    def test_would_default_value_worked(self,
                                        fix_create_all_tables
                                        ):
        """Confirm again the default values after insert into Database."""
        session = fix_create_all_tables

        user_1 = User(**self.user_1)
        session.add(user_1)
        session.commit()

        assert user_1.is_active
        assert not user_1.is_deleted
        assert user_1.created_by == 0
        assert user_1.last_updated_by == 0
        datetime_now = datetime.datetime.now()
        assert round(
            (datetime_now - user_1.created_on).total_seconds()
        ) == 0
        assert round(
            (datetime_now - user_1.last_updated_on).total_seconds()
        ) == 0

        user_2 = User(created_by_user_id=user_1.user_id, **self.user_2)
        session.add(user_2)
        session.commit()

        assert user_2.created_by == user_1.user_id
        assert user_2.last_updated_by == user_1.user_id

    def test_would_add_failed_on_duplicate_email(self, fix_create_all_tables):
        """No duplicate allowed in User table."""

        session = fix_create_all_tables

        session.add(User(**self.user_1))
        session.commit()

        with pytest.raises(IntegrityError):
            session.add(User(**self.user_1))
            session.commit()

        with pytest.raises(InvalidRequestError):
            session.add(User(**self.user_2))
            session.add(User(**self.user_2))
            session.commit()
