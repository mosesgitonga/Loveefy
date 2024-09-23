#!/usr/bin/env python3
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime, Float 
from sqlalchemy.orm import relationship
from .base_model import Base
import enum 
from datetime import datetime, timedelta

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(String(36), primary_key=True)
    amount = Column(Integer, nullable=False)
    time = Column(String(30), nullable=False)
    status = Column(String(15), nullable=False)
    method = Column(String(30), nullable=False)
    
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    user = relationship('User', backref='payments')


  


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String(36), primary_key=True)

    user_id = Column(String(36), ForeignKey('users.id'))
    plan_type = Column(String(15))
    transaction_type = Column(String(15))
    start_date = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime, index=True)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    phone_number = Column(String(17))
    transaction_id = Column(String(100), unique=True)
    status=Column(String(20))
    amount = Column(Float)

    user = relationship("User", backref="subscriptions")

