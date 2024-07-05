from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base_model import Base 

class User_profile(Base):
    __tablename__ = 'users_profile'

    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    gender = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    mobile_no = Column(String(16), unique=True, nullable=False, index=True)
    subscription_type = Column(String(15), nullable=False)
    industry_major = Column(String(25))
    fav_hobby = Column(String(20))
    has_child = Column(String(10), default='no')

    user_id = Column(String(36), ForeignKey('users.id'), unique=True, nullable=False, index=True)
    
    user = relationship("User", uselist=False, backref="profile")
