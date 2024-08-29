from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base_model import Base 

class User_profile(Base):
    __tablename__ = 'users_profile'

    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    gender = Column(String(20), nullable=False)
    DOB = Column(DateTime, nullable=False) # date of birth
    mobile_no = Column(String(16), unique=True, nullable=False, index=True)
    education_level = Column(String(36))
    industry_major = Column(String(25), nullable=False)
    employment = Column(String(25))
    is_schooling = Column(String(25))
    career = Column(String(50), nullable=True)
    has_child = Column(String(10), default='no')

    user_id = Column(String(36), ForeignKey('users.id'), unique=True, nullable=False, index=True)
    
    user = relationship("User", uselist=False, backref="profile")
