#!/usr/bin/env python3
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from .base_model import Base

class Upload(Base):
    __tablename__ = 'uploads'

    id = Column(String(60), primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    image_path = Column(String(200), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    is_primary = Column(Boolean, default=False)
    file_size = Column(String(50), nullable=True)

    user = relationship('User', back_populates="uploads")