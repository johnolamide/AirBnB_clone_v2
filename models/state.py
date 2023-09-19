#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(
        String(128),
        nullable=False
    )

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            "City", backref="state",
            cascade="all, delete-orphan"
        )
    else:
        @property
        def cities(self):
            """ Getter attribut to return a list
                of associated City instance
            """
            city_list = []
            for city_id, city in models.storage.all(models.City).items():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
