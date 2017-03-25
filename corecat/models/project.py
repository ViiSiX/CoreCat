from corecat.constants import OBJECT_CODES, MODEL_VERSION
from ._sqlalchemy import Base, CoreCatBaseMixin
from ._sqlalchemy import Column, \
    Integer, \
    String, Text


class Project(CoreCatBaseMixin, Base):
    """Project Model class represent for the 'projects' table
    which is used to store project's basic information."""

    # Add the real table name here.
    # TODO: Add the database prefix here
    __tablename__ = 'project'

    # Column definition
    project_id = Column('id', Integer,
                        primary_key=True,
                        autoincrement=True
                        )
    project_name = Column('name', String(100),
                          nullable=False
                          )
    project_description = Column('description', Text,
                                 nullable=True
                                 )

    # Relationship
    # TODO: Building relationship

    def __init__(self, project_name,
                 created_by_user_id,
                 **kwargs):
        """
        Constructor of Project Model Class.

        :param project_name: Name of the project.
        :param created_by_user_id: Project is created under this user ID.
        :param project_description: Description of the project.
        """

        self.set_up_basic_information(
            MODEL_VERSION[OBJECT_CODES['Project']],
            created_by_user_id
        )
        self.project_name = project_name
        self.project_description = kwargs.get('project_description', None)
