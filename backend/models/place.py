#!/usr/bin/env python3
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base_model import Base


class Place(Base):
    __tablename__ = 'places'
    id = Column(String(120), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    country = Column(String(150), nullable=False)
    region = Column(String(100), nullable=False)
    sub_region = Column(String(100), nullable=False)
    longitude = Column(Integer, nullable=True)
    latitude = Column(Integer, nullable=True)
 
    user_id = Column(String(120), ForeignKey('users.id'), nullable=False)
    user = relationship("User",  backref="places")
