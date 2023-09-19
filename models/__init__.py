#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""

import os
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


classes = {
    "State": State,
    "User": User,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}

storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
