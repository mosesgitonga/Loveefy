#!/usr/bin/env python3
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base_model import Base

class Matches(Base):
    __tablename__ = 'matches'
    id = Column(String(120), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_id1 = Column(String(120), ForeignKey('users.id'), nullable=False)
    user_id2 = Column(String(120), ForeignKey('users.id'), nullable=False)
    status = Column(String(120), nullable=False) # 'matched', 'pending', 'declined'

    #Foreign keys
    message_id = Column(String(120), ForeignKey('messages.id'), nullable=False)
    # relationships
    user1 = relationship("User", foreign_keys=[user_id1], backref="match_as_user_1")
    user2 = relationship("User", foreign_keys=[user_id2], backref="match_as_user_2")
    related_messages = relationship("Messages", backref="related_matches")
