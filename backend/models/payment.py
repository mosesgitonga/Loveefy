#!/usr/bin/env python3
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import Base

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(String(36), primary_key=True)
    amount = Column(Integer, nullable=False)
    time = Column(String(30), nullable=False)
    status = Column(String(15), nullable=False)
    method = Column(String(30), nullable=False)
    
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    user = relationship('User', backref='payments')
