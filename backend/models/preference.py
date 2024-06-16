#!/usr/bin/env python3
from .base_model import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
"""users preference model"""

class Preference(Base):
    __tablename__ = "preferences"
    id = Column(String(120), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    gender = Column(String(70), nullable=False)
    min_age = Column(Integer, default=18, nullable=False)
    max_age = Column(Integer, default=65, nullable=False)
    country = Column(String(120), nullable=True)
    region = Column(String(120), nullable=True)
    industry_major = Column(String(50))
    fav_hobby = Column(String(50))
    has_child = Column(String(40), default='no')
    wants_child = Column(String(40), default='yes')

    user_id = Column(String(120), ForeignKey('users.id'), nullable=False)

    user = relationship('User', uselist=False, backref='preferences')
