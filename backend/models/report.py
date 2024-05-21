#!/usr/bin/env python3
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import Base

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
