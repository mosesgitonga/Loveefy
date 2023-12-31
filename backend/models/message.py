#!/usr/bin/env python3
"""
users messages table class
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from datetime import datetime

#curr_time = datetime.datetime.now()
#str_date = curr_time.strftime("%Y-%m-%d")
#str_time = curr_time.strftime("%H-%M-%S")

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(String(200), primary_key=True)
    text = Column(String(1024), nullable=True)
    sender_id = Column(String(256), nullable=False)
    reciever_id = Column(String(256), nullable=False)
    