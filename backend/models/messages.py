from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .base_model import Base

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(String(36), primary_key=True)
    sender_Id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    receiver_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    content = Column(String(1024), nullable=False)
    time = Column(DateTime, default=func.now(), nullable=False)
    status = Column(String(20), nullable=True)
    room_id = Column(String(75), ForeignKey('rooms.id'), nullable=False)  # Adjusted length for concatenated UUIDs

    sender = relationship("User", foreign_keys=[sender_Id], backref="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], backref='received_messages')

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(String(75), primary_key=True)  # Adjusted length for concatenated UUIDs
    name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    members = Column(String(200), nullable=True)

    messages = relationship('Messages', backref='room')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name, 
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class RoomMember(Base):
    __tablename__ = "room_members"
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    room_id = Column(String(75), ForeignKey('rooms.id'), nullable=False, index=True)  # Adjusted length for concatenated UUIDs
