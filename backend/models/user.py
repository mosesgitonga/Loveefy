#!/user/bin/env python3
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String(200), primary_key=True, default=str(uuid.uuid4()))
    username = Column(String(200), unique=True, nullable=False)
    gender = Column(String(50), nullable=False)
    county = Column(String(70), nullable=False)
    physical_addr = Column(String(150), nullable=False)
    phone_num = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String(256), nullable=False)
    bio = Column(String(270), unique=True, nullable=True)
    profile_pic = Column(String(270), nullable=True)
    email = Column(String(256), unique=True, nullable=False)