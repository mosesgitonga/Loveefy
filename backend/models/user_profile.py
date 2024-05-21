from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import Column, String, Integer
from .base_model import Base

class User_profile(Base):
    __tablename__ = 'users_profile'
    id = Column(String(120), primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    gender = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    mobile_no = Column(String(120), unique=True, nullable=False)
    subscription_type = Column(String(60), nullable=False)

    user_id = Column(String(120), ForeignKey('users.id'), nullable=False)
    place_id = Column(String(120), ForeignKey('places.id'))

    user = relationship("User", uselist=False, backref="users_profile")
    place = relationship("Place", uselist=False, backref="users_profile")
