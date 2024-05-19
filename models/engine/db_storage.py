#!/usr/bin/python3
"""
Module for managing database storage
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

CLASSES = {
    "Amenity": models.amenity.Amenity,
    "City": models.city.City,
    "Place": models.place.Place,
    "Review": models.review.Review,
    "State": models.state.State,
    "User": models.user.User
}

class DBStorage:
    """Interacts with the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, database),
            pool_pre_ping=True
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        for clss in CLASSES:
            if cls is None or cls is CLASSES[clss] or cls is clss:
                objs = self.__session.query(CLASSES[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id_value):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in CLASSES.values():
            return None
        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id_value:
                return value
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage
        """
        all_classes = CLASSES.values()
        if cls is None:
            count = 0
            for class_obj in all_classes:
                count += len(models.storage.all(class_obj).values())
        else:
            count = len(models.storage.all(cls).values())
        return count
