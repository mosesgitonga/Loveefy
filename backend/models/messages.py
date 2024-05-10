from sqlalchemy import Column, String
from .base_model import Base

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(String(120), primary_key=True)
    senderId = Column(String(120), nullable=False)
    receiver_id = Column(String(120), nullable=False)
    content = Column(String(1024), nullable=False)
    time = Column(String(120), nullable=False)
    status = Column(String(70), nullable=False) # read, unread
