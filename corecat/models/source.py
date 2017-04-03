from corecat.constants import MODEL_VERSION, OBJECT_CODES, \
    SOURCE_TYPE_CODES, ATTRIBUTE_TYPES
from ._sqlalchemy import Base, CoreCatBaseMixin, ProxyDictMixin
from ._sqlalchemy import relationship, backref, \
    collections, association_proxy, \
    hybrid_property
from ._sqlalchemy import Column, ForeignKey, \
    Integer, SmallInteger, \
    String


class SourceBase(CoreCatBaseMixin, ProxyDictMixin, Base):
    """Source Model Base class represent for the 'source_base' table
    which is used to store data sources."""

    # Add the real table name here.
    # TODO: Add the database prefix here
    __tablename__ = 'source_base'

    # Column definition
    source_id = Column('id', Integer,
                       primary_key=True,
                       autoincrement=True
                       )
    source_name = Column('name', String(100),
                         nullable=False
                         )
    source_type = Column('type', SmallInteger,
                         nullable=False
                         )

    # Proxy
    _proxy_obj = association_proxy("source_attributes",
                                   "attribute_value",
                                   creator=lambda name, value:
                                   SourceAttribute(
                                       attribute_name=name,
                                       attribute_value=value,
                                   ))

    # Mapper class to identify the type of data source
    __mapper_args__ = {
        'polymorphic_on': source_type,
        'polymorphic_identity': SOURCE_TYPE_CODES['Base']
    }

    def __init__(self, source_name,
                 source_type,
                 created_by_user_id
                 ):
        """
        Construction for Source Model Class.

        :param source_name: Name of the data source.
        :type source_name: str
        :param source_type: Type of the data source.
        :type source_type: int
        :param created_by_user_id: created under this user Id.
        :type created_by_user_id: int
        """

        self.set_up_basic_information(
            MODEL_VERSION[OBJECT_CODES['Source']],
            created_by_user_id
        )
        self.source_name = source_name
        self.source_type = source_type


class SourceAttribute(Base):
    """Other attributes for Source Model which is not
    stored on 'source_base' table."""

    __tablename__ = 'source_attribute'

    source_id = Column('sourceId', Integer,
                       ForeignKey(SourceBase.source_id),
                       primary_key=True
                       )
    attribute_name = Column('attributeName', String(255),
                            primary_key=True
                            )
    attribute_type = Column('attributeType', String(20),
                            nullable=False
                            )
    _attribute_value = Column('attributeValue', String(255),
                              nullable=False
                              )

    def __init__(self, attribute_name, attribute_value):
        """
        Constructor class of SourceAttribute model class.

        :param attribute_name: Name of the attribute.
        :param attribute_value: Value of the attribute (in many type).
        """

        self.attribute_name = attribute_name
        self.attribute_value = attribute_value

    @hybrid_property
    def attribute_value(self):
        """Convert attribute value to it's type then return."""
        return ATTRIBUTE_TYPES['StringToType'][self.attribute_type](
            self._attribute_value
        )

    @attribute_value.setter
    def attribute_value(self, attribute_value):
        """Detect a given value and save it."""
        self.attribute_type = ATTRIBUTE_TYPES['TypeToString'][type(
            attribute_value
        )]
        self._attribute_value = str(attribute_value)


# Relationship between SourceBase and SourceAttribute
SourceBase.source_attributes = relationship(
    SourceAttribute,
    collection_class=collections.attribute_mapped_collection(
        "attribute_name"
    )
)
