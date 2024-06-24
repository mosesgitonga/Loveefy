#!/usr/bin/env python3
from .base_model import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
"""users preference model"""

class Preference(Base):
    __tablename__ = "preferences"
    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    gender = Column(String(25), nullable=False, index=True)
    min_age = Column(Integer, default=18, nullable=True)
    max_age = Column(Integer, default=65, nullable=True)
    country = Column(String(30), nullable=True, index=True)
    region = Column(String(30), nullable=True)
    industry_major = Column(String(50), default='any', nullable=True, index=True)
    fav_hobby = Column(String(50))
    wants_child = Column(String(25), default='any')

    user = relationship("User", uselist=False, back_populates="preference")


