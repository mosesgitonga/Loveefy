from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base_model import Base


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(String(120), primary_key=True)
    sender_Id = Column(String(120), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(String(120), ForeignKey('users.id'), nullable=False)
    content = Column(String(1024), nullable=False)
    time = Column(DateTime, nullable=False)
    status = Column(String(70), nullable=False) # read, unread

    sender = relationship("User", foreign_keys=[sender_Id],backref="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], backref='received_messages')