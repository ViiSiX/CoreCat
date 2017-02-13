from sys import version_info
import datetime
from corecat import constants
from corecat import utils
from corecat.models import Base
from corecat.models import Column, \
    Boolean, Integer, \
    String, \
    DateTime


class User(Base):
    """The User class represent for the User table
    containing a user's information."""

    # Add the real table name here.
    # TODO: Add the database prefix here
    __tablename__ = 'users'

    # Column definition
    user_id = Column('id', Integer,
                     primary_key=True,
                     autoincrement=True
                     )
    email = Column('emailAddress', String(255),
                   index=True,
                   unique=True,
                   nullable=False
                   )
    password = Column('password', String(255),
                      nullable=False
                      )
    is_active = Column('isActive', Boolean,
                       nullable=False,
                       default=True
                       )
    created_on = Column('createdOn', DateTime,
                        default=datetime.datetime.now)
    last_login = Column('lastLoginOn', DateTime,
                        nullable=True)
    last_updated_on = Column('lastUpdatedOn',
                             DateTime,
                             onupdate=datetime.datetime.now,
                             default=datetime.datetime.now)
    _version = Column('version', Integer,
                      index=False, nullable=False)

    # Relationship
    # TODO: Building relationship
    # connections = relationship('Connection',
    #                            backref='User',
    #                            lazy='joined')
    # jobs = relationship('Job',
    #                     backref='User',
    #                     lazy='joined')

    def __init__(self, user_email, user_password):
        """
        Constructor for User class.

        :param user_email: User's email.
        :param user_password: User's password in clear text.
        """

        self._version = constants.MODEL_VERSION[self.__class__.__name__]

        if utils.is_valid_format_email(user_email):
            self.email = user_email
        else:
            raise ValueError('Email %s is not valid!' % user_email)
        self.password = utils.encrypt_password(user_password)

    def get_id(self):
        """Get the user id in unicode string."""

        if self.user_id is None:
            return ''
        if version_info >= (3, 0):
            return str(self.user_id)
        return unicode(self.user_id)

    def __repr__(self):
        """Print the User instance."""

        return '<Corecat.User {email} - Id {id}>'.format(
            email=self.email,
            id=self.user_id
        )
