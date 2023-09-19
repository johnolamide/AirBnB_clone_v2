#!/usr/bin/python3
""" Module contains the class definition for DBStorage Engine
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import DeclarativeMeta
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv


class DBStorage:
    """ Database storage class"""

    __engine = None
    __session = None

    def __init__(self):
        """ Initialize DBStorage instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the database"""

        objects = {}
        if cls:
            #if isinstance(cls, str):
            #    cls = classes.get(cls, None)
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            classes = [User, State, City, Amenity, Place, Review]
            for cls in classes:
                if isinstance(cls, DeclarativeMeta):
                    query = self.__session.query(cls).all()
                    for obj in query:
                        key = "{}.{}".format(type(obj).__name__, obj.id)
                        objects[key] = obj
        return objects

    def new(self, obj):
        """Add an object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
