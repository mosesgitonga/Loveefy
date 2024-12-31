from sqlalchemy import Column, String, DateTime, ForeignKey, func, Text, Boolean
from sqlalchemy.orm import relationship
from .base_model import Base

class User_profile(Base):
    __tablename__ = 'users_profile'

    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    first_name = Column(String(30), nullable=False)
    gender = Column(String(20), nullable=False)
    DOB = Column(DateTime, nullable=False)  # Date of Birth
    education_level = Column(String(36))
    institution = Column(String(50), nullable=False)
    industry_major = Column(String(25), nullable=False) 
    is_schooling = Column(Boolean)
    occupation = Column(String(50), nullable=True)
    career_goals = Column(String(150))
    about_me = Column(Text) 
    personality = Column(String(30)) 
    has_child = Column(Boolean)
    spiritual_beliefs = Column(String(20)) 
    favourite_music_genre = Column(String(20))
    love_language = Column(String(30)) # eg. quality time
    achievements = Column(Text)
    linkedIn_profile = Column(Text) 

    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    user = relationship("User", back_populates="profile")
