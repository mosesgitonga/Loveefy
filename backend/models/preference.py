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
    career = Column(String(36))
    education_level = Column(String(40), default='any')
    employment = Column(String(20))
    is_schooling = Column(String(10))
    fav_hobby = Column(String(50))
    wants_child = Column(String(25), default='any')

    user = relationship("User", uselist=False, back_populates="preference")

    def serialize(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "min_age": self.min_age,
            "max_age": self.max_age,
            "country": self.country,
            "region": self.region,
            "industry_major": self.industry_major,
            "career": self.career,
            "education_level": self.education_level,
            "employment": self.employment,
            "is_schooling": self.is_schooling,
            "fav_hobby": self.fav_hobby,
            "wants_child": self.wants_child
        }


