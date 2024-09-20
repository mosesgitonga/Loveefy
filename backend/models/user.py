from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base_model import Base
import uuid

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    email = Column(String(254), nullable=False, unique=True, index=True)
    password = Column(String(150), nullable=False)
    username = Column(String(80), unique=True, nullable=False, index=True)

    place_id = Column(String(36), ForeignKey('places.id'), index=True)
    place = relationship("Place", back_populates="user", uselist=False)

    preference_id = Column(String(36), ForeignKey('preferences.id'), nullable=True, index=True)
    preference = relationship("Preference", uselist=False, back_populates="user")

    profile = relationship("User_profile", back_populates="user", cascade="all, delete-orphan", uselist=False)

    uploads = relationship("Upload", back_populates="user", cascade="all, delete-orphan")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "place_id": self.place_id,
            "preference_id": self.preference_id
        }
    
class Otp(Base):
    __tablename__ = "otp"
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)
    otp = Column(String(10))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    exp = Column(DateTime)
    email = Column(String(36), ForeignKey('users.email'), nullable=False, index=True)




