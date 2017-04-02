from sys import version_info
from corecat.constants import OBJECT_CODES, MODEL_VERSION
from corecat import utils
from ._sqlalchemy import Base, CoreCatBaseMixin
from ._sqlalchemy import Column, \
    Integer, \
    String, \
    DateTime


class User(CoreCatBaseMixin, Base):
    """The User class represent for the 'user' table
    containing a user's information."""

    # Add the real table name here.
    # TODO: Add the database prefix here
    __tablename__ = 'user'

    # Column definition
    user_id = Column('id', Integer,
                     primary_key=True,
                     autoincrement=True
                     )
    user_email = Column('emailAddress', String(255),
                        index=True,
                        unique=True,
                        nullable=False
                        )
    password = Column('password', String(255),
                      nullable=False
                      )
    last_login = Column('lastLoginOn', DateTime,
                        nullable=True)

    # Relationship
    # TODO: Building relationship

    def __init__(self, user_email, user_password,
                 created_by_user_id=0):
        """
        Constructor for User Model class.

        :param user_email: User's email.
        :param user_password: User's password in clear text.
        :param created_by_user_id: User is created under this user id.
        """

        self.set_up_basic_information(
            MODEL_VERSION[OBJECT_CODES['User']],
            created_by_user_id
        )

        if utils.validate_format_email(user_email):
            self.user_email = user_email
        else:
            raise ValueError('Email {0} is not valid!'.format(user_email))
        self.password = utils.encrypt_password(user_password)

    def get_id(self):
        """Get the user id in unicode string. This is the standard for later
        changes that ID would always be a string for upper layers."""

        if self.user_id is None:
            return ''
        if version_info >= (3, 0):
            return str(self.user_id)
        return unicode(self.user_id)

    def __repr__(self):
        """Print the User instance."""

        return '<Corecat.User {email} - Id {id}>'.format(
            email=self.user_email,
            id=self.user_id
        )
