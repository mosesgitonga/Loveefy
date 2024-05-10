from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User_profile(Base):
    __tablename__ = 'users_profile'
    id = Column(String, primary_key=True)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    mobile_no = Column(String, unique=True, nullable=False)
