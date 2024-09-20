#!/usr/bin/env python3
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base_model import Base
import uuid

class Reports(Base):
    """
    model for reporting a user.
    """
    __tablename__ = 'reports'
    id = Column(String(120), primary_key=True)
    reporter_id = Column(String(120), ForeignKey('users.id'), nullable=False)
    reported_id = Column(String(120), ForeignKey('users.id'), nullable=False)
    reason = Column(String(400), nullable=False)
    time = Column(String(50), nullable=False)
    status = Column(String(30), nullable=False) # pending, resolved

    reporter = relationship('User', foreign_keys=[reporter_id], backref="reporter")
    reported_user = relationship("User", foreign_keys=[reported_id], backref='reported')

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(120), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    remarks = Column(String(300), nullable=False)
    ratings = Column(Integer, nullable=True)
    suggestions = Column(String(200), nullable=True)

    user = relationship('User', back_populates="feedback")
