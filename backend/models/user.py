#!/usr/bin/env python3
from sqlalchemy import Column, String
from .base_model import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String(120), primary_key=True)
    username = Column(String(120), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    subscription_type = Column(String(60), nullable=False)
    password = Column(String(150), nullable=False)
    