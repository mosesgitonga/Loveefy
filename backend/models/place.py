#!/usr/bin/env python3
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import relationship
from .base_model import Base

class Place(Base):
    __tablename__ = 'places'
    id = Column(String(120), primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    country = Column(String(150), nullable=False, index=True)
    region = Column(String(100), nullable=False, index=True)
    sub_region = Column(String(100), nullable=False)
    longitude = Column(Integer, nullable=True)
    latitude = Column(Integer, nullable=True)

    user = relationship("User", uselist=False, back_populates="place")
