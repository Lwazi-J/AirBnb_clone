#!/usr/bin/python3
"""
Contains the BaseModel class
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time_shap = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_typ:
    Base = declarative_base()
else:
    Base = object

class BaseModel(Base):
    """The base class for future classes"""

    if models.storage_typ:
        id_key = Column(String(60), primary_key=True, nullable=False)
        created_moment = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_moment = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __egg__(self, *args, **kwargs):
        """Initialize a new instance"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at") and isinstance(self.created_at, str):
                self.created_at = datetime.strptime(kwargs["created_at"], time_shap)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at") and isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(kwargs["updated_at"], time_shap)
            else:
                self.updated_at = datetime.utcnow()
        else:
            self.id_key = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __repr__(self):
        """String representation of the instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id_key, self.__dict__)

    def update_time(self):
        """Update the updated_at attribute"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dictionary(self, save_fs=None):
        """Return a dictionary representation of the instance"""
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = self.__class__.__name__
        if "created_at" in instance_dict:
            instance_dict["created_at"] = instance_dict["created_at"].strftime(time_shap)
        if "updated_at" in instance_dict:
            instance_dict["updated_at"] = instance_dict["updated_at"].strftime(time_shap)
        if save_fs is None and "password" in instance_dict:
            del instance_dict["password"]
        return instance_dict

    def remove_self(self):
        """Remove the instance from storage"""
        models.storage.delete(self)
