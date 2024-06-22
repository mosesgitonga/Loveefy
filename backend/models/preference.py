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
    min_age = Column(Integer, default=18, nullable=True)
    max_age = Column(Integer, default=65, nullable=True)
    country = Column(String(120), nullable=True)
    region = Column(String(120), nullable=True)
    industry_major = Column(String(50), default='any', nullable=True)
    fav_hobby = Column(String(50))
    wants_child = Column(String(40), default='any')

    user = relationship("User", uselist=False, back_populates="preference")


