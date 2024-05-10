#!/usr/bin/env python3
from sqlalchemy import Column, String
from .base_model import Base

class Matches(Base):
    __tablename__ = 'matches'
    id = Column(String(120), primary_key=True)
    user_id1 = Column(String(120), nullable=False)
    user_id2 = Column(String(120), nullable=False)
    status = Column(String(120), nullable=False) # 'matched', 'pending', 'declined'
