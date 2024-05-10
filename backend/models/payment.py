#!/usr/bin/env python3
from sqlalchemy import Column, String, Integer
from .base_model import Base

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(String(120), primary_key=True)S
    user_id = Column(String(120), nullable=False)
    amount = Column(Integer, nullable=False)
    time = Column(String(79), nullable=False)
    status = Column(String(50), nullable=False)
    method = Column(String(67), nullable=False)
