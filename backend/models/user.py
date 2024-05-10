#!/usr/bin/env python3
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String(120), primary_key=True)
    username = Column(String(120), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    subscription_type = Column(String(60), nullable=False)