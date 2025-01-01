from sqlalchemy import Column, String, DateTime, Enum, func
import enum
import uuid
from .base_model import Base

class PowerLevel(enum.Enum):
    ORDINARY = "ordinary"
    MODERATE = "moderate"
    SUPER = "super"

class Admin(Base):
    __tablename__ = "admins"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    name = Column(String(25), nullable=False)
    
    power = Column(Enum(PowerLevel, name="power_level"), default=PowerLevel.ORDINARY, nullable=False)
    
    email = Column(String(60), unique=True, nullable=False)
    
    password = Column(String(254), nullable=False)  
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
