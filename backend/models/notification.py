from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref
import uuid
from .base_model import Base

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_to_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    user_from_id = Column(String(36), ForeignKey('users.id'), nullable=True, index=True)
    message = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships with User
    user_to = relationship('User', foreign_keys=[user_to_id], backref=backref("notifications_to", lazy='dynamic'))
    user_from = relationship('User', foreign_keys=[user_from_id], backref=backref("notifications_from", lazy='dynamic'))

    def __repr__(self):
        return f"<Notification(id='{self.id}', user_to_id='{self.user_to_id}', message='{self.message}')>"
