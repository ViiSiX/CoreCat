from corecat.constants import OBJECT_CODES, MODEL_VERSION
from ._sqlalchemy import Base, CoreCatBaseMixin
from ._sqlalchemy import Column, \
    Integer, \
    String, Text


class Directory(CoreCatBaseMixin, Base):
    """
    Directory Model class represent for the 'directory' table
    which is used to store directory's basic information.

    Directory is the place where users can create and share
    resources to users and groups.
    """

    __tablename__ = 'directory'

    directory_id = Column('id', Integer,
                          primary_key=True,
                          autoincrement=True
                          )
    directory_name = Column('name', String(100),
                            nullable=False,
                            )
    directory_description = Column('description', Text,
                                   nullable=True
                                   )

    def __init__(self, directory_name, created_by_user_id, **kwargs):
        """
        Constructor of Directory Model class.

        :param directory_name: Name of the directory.
        :param created_by_user_id: Project is created under this user ID.
        :param directory_description: Description of the directory.
        """

        self.set_up_basic_information(
            MODEL_VERSION[OBJECT_CODES['Directory']],
            created_by_user_id
        )
        self.directory_name = directory_name
        self.directory_description = kwargs.get('directory_description')
