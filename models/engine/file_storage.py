#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
import models
from hashlib import md5

class_dict = {
    "Amenity": models.amenity.Amenity,
    "BaseModel": models.base_model.BaseModel,
    "City": models.city.City,
    "Place": models.place.Place,
    "Review": models.review.Review,
    "State": models.state.State,
    "User": models.user.User
}


class FileStorage:
    """Serializes instances to a JSON file
    and deserializes back to instances"""

    # Path to the JSON file
    __file_location = "file.json"

    # Dictionary to store all objects
    __storage = {}

    def all(self, cls=None):
        """Returns the __storage dictionary"""
        if cls is None:
            return self.__storage
        filtered_dict = {}
        for key, value in self.__storage.items():
            if value.__class__ == cls or value.__class__.__name__ == cls:
                filtered_dict[key] = value
        return filtered_dict

    def new(self, obj):
        """Sets the obj in __storage with key <obj class name>.id"""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id_key}"
            self.__storage[key] = obj

    def save(self):
        """Serializes __storage to the JSON file"""
        json_objects = {}
        for key, value in self.__storage.items():
            json_objects[key] = value.to_dictionary(save_fs=1)

        with open(self.__file_location, 'w') as file:
            json.dump(json_objects, file)

    def reload(self):
        """Deserializes the JSON file to __storage"""
        try:
            with open(self.__file_location, 'r') as file:
                json_data = json.load(file)
            for key, value in json_data.items():
                class_name = value["__class__"]
                del value["__class__"]
                self.__storage[key] = class_dict[class_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __storage if it exists"""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id_key}"
            if key in self.__storage:
                del self.__storage[key]

    def reload_data(self):
        """Calls reload() method to deserialize the JSON file"""
        self.reload()

    def get(self, cls, id_value):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in class_dict.values():
            return None
        all_cls = self.all(cls)
        for obj in all_cls.values():
            if obj.id_key == id_value:
                return obj
        return None

    def count(self, cls=None):
        """
        Counts the number of objects in storage
        """
        if cls is None:
            count = 0
            for class_obj in class_dict.values():
                count += len(self.all(class_obj).values())
            return count
        else:
            return len(self.all(cls).values())
