#!/usr/bin/env python3
from sqlalchemy import Column, String
from .base_model import Base

class Reports(Base):
    """
    model for reporting a user.
    """
    __tablename__ = 'reports'
    id = Column(String(120), primary_key=True)
    reporter_id = Column(String(120), nullable=False)
    reported_id = Column(String(120), nullable=False)
    reason = Column(String(400), nullable=False)
    time = Column(String(50), nullable=False)
    status = Column(String(30), nullable=False) # pending, resolved
