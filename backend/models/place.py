#!/usr/bin/env python3
from sqlalchemy import Column, String, Integer
from .base_model import Base


class Place(Base):
    __tablename__ = 'places'
    id = Column(String(120), primary_key=True)
    user_id = Column(String(120), nullable=False)
    country = Column(String(150), nullable=False)
    region = Column(String(100), nullable=False)
    sub_region = Column(String(100), nullable=False)
    longitude = Column(Integer, nullable=True)
    latitude = Column(Integer, nullable=True)
