#!/usr/bin/env python3
from sqlalchemy import Column, String
from .base_model import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String(120), primary_key=True, index=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
