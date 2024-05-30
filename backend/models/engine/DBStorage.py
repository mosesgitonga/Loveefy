from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask
from dotenv import load_dotenv
from models.base_model import Base
from models.user_profile import User_profile
import os

load_dotenv()

class DbStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
        self.__engine = create_engine(self.db_uri)
        self.sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.Session = scoped_session(self.sess_factory)
        self.__session = self.Session

    def reload(self):
        """reloads data from database"""
        try:
            Base.metadata.create_all(self.__engine)
            sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
            Session = scoped_session(sess_factory)
            if Session is None:
                print('Did not create session')
                return
            print('session created successfully')
            self.__session = Session
        except Exception as e:
            print(f'An Error occured while reloading {e}')

    def new(self, obj):
        # add obj to current db session
        self.__session.add(obj)

    def save(self):
        'commits changes to db'
        self.__session.commit()

    def delete(self, obj=None):
        'delete the current db session obj'
        self.__session.delete(obj)

    def get(self, cls=None, **kwargs):
        'it returns an object based on the class and  key word argument'
        if not cls:
            return None

        if 'username' in kwargs:
            return self.__session.query(cls).filter_by(username=kwargs['username']).first()
        if 'email' in kwargs:
            return self.__session.query(cls).filter_by(email=kwargs['email']).first()
        if 'mobile_no' in kwargs:
            return self.__session.query(cls).filter_by(mobile_no=kwargs['mobile_no']).first()
        if 'id' in kwargs:
            return self.__session.query(cls).filter_by(id=kwargs['id']).first()

    def check_existing_profile(self, user_id, username, mobile_no):
        return self.__session.query(User_profile).filter(
            (User_profile.user_id == user_id) | 
            (User_profile.username == username) |
            (User_profile.mobile_no == mobile_no)
        ).first()
