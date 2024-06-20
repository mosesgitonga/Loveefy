#!/usr/bin/env python3
from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base_model import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String(120), primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    password = Column(String(150), nullable=False)
    username = Column(String(80), unique=True, nullable=False, index=True)

    place_id = Column(String(120), ForeignKey('places.id'), nullable=True)
    place = relationship("Place", uselist=False, back_populates="user")
