#!/usr/bin/python3
"""
Initialize the models package
"""

from os import getenv

storage_typ = getenv("HBNB_TYPE_STORAGE")

if storage_typ == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload_data()
