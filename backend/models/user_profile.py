from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, String, Integer
from .base_model import Base

class User_profile(Base):
    __tablename__ = 'users_profile'
    id = Column(String(120), primary_key=True)
    gender = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    mobile_no = Column(String(120), unique=True, nullable=False)
