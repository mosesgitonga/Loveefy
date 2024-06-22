from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import Column, String, Integer, DateTime
from .base_model import Base

class User_profile(Base):
    __tablename__ = 'users_profile'
    id = Column(String(120), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    gender = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    mobile_no = Column(String(120), unique=True, nullable=False)
    subscription_type = Column(String(60), nullable=False)
    industry_major = Column(String(50))
    fav_hobby = Column(String(50))
    has_child = Column(String(40), default='no')

    user_id = Column(String(120), ForeignKey('users.id'), nullable=False)

    user = relationship("User", uselist=False, backref="users_profile")
