"""Basic import and mixin classes."""

import datetime
from sqlalchemy.ext.declarative import declarative_base, \
    as_declarative
from sqlalchemy.orm import relationship, backref, \
    collections
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, \
    ForeignKey, UniqueConstraint, \
    Boolean, \
    Integer, SmallInteger, BigInteger, \
    String, Text, \
    DateTime


Base = declarative_base()


class ProxyDictMixin(object):  # pragma: no cover
    """Adds obj[key] access to a mapped class.

    This class basically proxies dictionary access to an attribute
    called ``_proxy_obj``.  The class which inherits this class
    should have an attribute called ``_proxy_obj`` which points to a
    dictionary.
    """

    _proxy_obj = {}

    def __len__(self):
        return len(self._proxy_obj)

    def __iter__(self):
        return iter(self._proxy_obj)

    def __getitem__(self, key):
        return self._proxy_obj[key]

    def __contains__(self, key):
        return key in self._proxy_obj

    def __setitem__(self, key, value):
        self._proxy_obj[key] = value

    def __delitem__(self, key):
        del self._proxy_obj[key]


@as_declarative()
class CoreCatBaseMixin(object):
    """This class is the skeleton for other Models."""

    # Automatic Column definition
    created_by = Column('createdBy', Integer,
                        nullable=False,
                        default=0)
    created_on = Column('createdOn', DateTime,
                        default=datetime.datetime.now)
    last_updated_by = Column('lastUpdatedBy', Integer,
                             nullable=False,
                             default=0)
    last_updated_on = Column('lastUpdatedOn', DateTime,
                             onupdate=datetime.datetime.now,
                             default=datetime.datetime.now)
    is_active = Column('isActive', Boolean,
                       nullable=False,
                       default=True
                       )
    is_deleted = Column('isDeleted', Boolean,
                        nullable=False,
                        default=False
                        )
    _version = Column('version', Integer,
                      index=False,
                      nullable=False,
                      )

    def set_up_basic_information(self, version, created_by_user_id):
        """In this function set up some basic information of Models Classes."""
        self._version = version
        self.created_by = created_by_user_id
        self.last_updated_by = created_by_user_id
