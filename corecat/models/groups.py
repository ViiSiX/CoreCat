from corecat.constants import MODEL_VERSION, OBJECT_CODES
from ._sqlalchemy import Base, CoreCatBaseMixin
from ._sqlalchemy import Column, ForeignKey, UniqueConstraint, \
    Integer, \
    String
from .directory import Directory


class Group(CoreCatBaseMixin, Base):
    """
    Group Model class represent for the 'group' table
    which is used to store group's basic information.

    Group is a set of users which is used to manage and sharing resources.
    """

    __tablename__ = 'group'

    group_id = Column('id', Integer,
                      primary_key=True,
                      autoincrement=True
                      )
    group_name = Column('name', String(100),
                        nullable=False
                        )
    directory_id = Column('directoryId', Integer,
                          ForeignKey(Directory.directory_id),
                          nullable=True
                          )

    group_directory_unq_constraint = UniqueConstraint(
        group_name, directory_id, name='unq_1_group_directory'
    )

    def __init__(self, group_name,
                 created_by_user_id,
                 directory_id=None,
                 **kwargs):
        """
        Constructor of Group Model class.

        :param group_name: Name of group.
        :param created_by_user_id: Group created under this user Id.
        :param directory_id: ID of the directory this group is under.
        :param kwargs: Other parameters.
        """

        self.group_name = group_name
        self.directory_id = directory_id
        self.set_up_basic_information(
            MODEL_VERSION[OBJECT_CODES['Group']],
            created_by_user_id
        )
