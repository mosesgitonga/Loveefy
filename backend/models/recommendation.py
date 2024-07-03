#!/usr/bin/env python3
from models.base_model import Base
from sqlalchemy import String, Integer, DateTime, func, ForeignKey, Column


class Recommendation(Base):
    __tablename__ = 'recommendations'
    id=Column(String(36), primary_key=True)
    user_id1 = Column(String(36), ForeignKey('users.id'), index=True)
    user_id2 = Column(String(36), ForeignKey('users.id'), index=True)
    score = Column(Integer, index=True)

    