#!/usr/bin/env python3
from .base_model import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
"""users preference model"""

class Preference(Base):
    __tablename__ = "preferences"
    id = Column(String(120), primary_key=True)
    gender = Column(String(70), nullable=False)
    min_age = Column(Integer, default=18, nullable=False)
    max_age = Column(Integer, default=65, nullable=False)
    country = Column(String(120), nullable=True)
    region = Column(String(120), nullable=True)

    user_profile_id = Column(String(120), ForeignKey('user_profile.id'), nullable=False)

    user_profile = relationship('User_profile', uselist=False, backref='preferences')
