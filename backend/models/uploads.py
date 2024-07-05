#!/usr/bin/env python3
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from .base_model import Base

class Upload(Base):
    __tablename__ = 'uploads'

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    image_path = Column(String(200), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    is_primary = Column(Boolean, default=False)
    file_size = Column(String(12), nullable=True)

    user = relationship('User', back_populates="uploads")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_path": self.image_path,
            "is_primary": self.is_primary,
            "file_size": self.file_size
        }