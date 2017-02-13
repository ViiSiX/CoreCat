import pytest
from corecat.models.user import User
from corecat import constants
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
        user = User(**self.user_1)

        assert user.email == self.user_1['user_email']
        assert user.password
        assert utils.check_password(
            user.password, self.user_1['user_password']
        )
        assert user._version == \
            constants.MODEL_VERSION[User.__name__]

    def test_would_init_fail_on_user_email(self):
        with pytest.raises(ValueError) as except_info:
            user = User(
                'mail_ops', 'password'
            )
        assert 'Email mail_ops is not valid!' in str(except_info)

    def test_would_init_fail_on_user_password(self):
        with pytest.raises(TypeError) as exec_info:
            user = User(
                'mail_ok@mail.mail', None
            )
        assert 'Password should be a string!' in str(exec_info)

    def test_would_get_id_return_an_empty_string(self):
        user = User(**self.user_1)

        assert user.get_id() == ''

    def test_would_get_id_after_add_user(self, fix_test_create_user_table):
        session = fix_test_create_user_table

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
