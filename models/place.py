#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
import os
from models.user import User
from models.city import City
from models.engine.file_storage import FileStorage
from sqlalchemy import ForeignKey, Column, String, Float, Integer
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id', ondelete='CASCADE'),
                     nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    storage_type = os.getenv("HBNB_TYPE_STORAGE")

    if storage_type == 'db':
        reviews = relationship("Review", backref="place",
                               cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)

    if storage_type == 'file':
        amenity_ids = []

        @property
        def reviews(self):
            """Getter of review instances"""
            from models.review import Review
            return [inst for inst in FileStorage.all(Review)
                    if inst.place_id == self.id]

        @property
        def amenities(self):
            """Getter for amenities"""
            return [inst for inst in FileStorage.all(Amenity).values()
                    if inst.amenity_id == self.id]

        @amenities.setter
        def amenities(self, obj=None):
            """Setter for Amenities"""
            if obj.__class__.__name__ == "Amenity":
                self.amenity_ids.append(obj.id)
