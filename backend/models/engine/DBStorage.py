from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask
from dotenv import load_dotenv
from models.base_model import Base
import os

load_dotenv()

class DbStorage:
    __engine = None
    __session = None


    def __init__(self):
        self.db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
        self.__engine = create_engine(self.db_uri)

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

    



storage = DbStorage()
storage.reload()