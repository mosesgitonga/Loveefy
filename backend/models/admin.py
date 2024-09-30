from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.mysql import ENUM as MysqlEnum
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
    
    # Use MySQL-specific ENUM type
    power = Column(MysqlEnum(PowerLevel), default=PowerLevel.ORDINARY)
    
    email = Column(String(60), unique=True, nullable=False)
    
    password = Column(String(254), nullable=False)  
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
