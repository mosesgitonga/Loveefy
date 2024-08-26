#!/usr/bin/env python3
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
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


# Enum for plan types
class PlanType(enum.Enum):
    FREE = "Free"
    PREMIUM = "Premium"
    ELITE = "Elite"

# Enum for transaction types
class TransactionType(enum.Enum):
    SIGNUP = "Signup"
    UPGRADE = "Upgrade"
    RENEWAL = "Renewal"

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String(36), primary_key=True)

    user_id = Column(String(36), ForeignKey('users.id'))
    plan_type = Column(Enum(PlanType), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False, index=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime, nullable=False, index=True)
    transaction_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="subscriptions")

    def __init__(self, user_id, plan_type, transaction_type, duration_days):
        self.user_id = user_id
        self.plan_type = plan_type
        self.transaction_type = transaction_type
        self.start_date = datetime.utcnow()
        self.expiration_date = self.start_date + timedelta(days=duration_days)
        self.transaction_date = datetime.utcnow()
