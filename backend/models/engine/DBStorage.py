from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from contextlib import contextmanager
from dotenv import load_dotenv
import os
import logging
from models.base_model import Base
from models.user_profile import User_profile
from models.uploads import Upload

logging.basicConfig(level=logging.INFO)
load_dotenv()

class DbStorage:
    def __init__(self):
        self.db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
        self.__engine = create_engine(
            self.db_uri,
            pool_size=20,
            max_overflow=30,
            pool_timeout=25,
            pool_recycle=3600
        )
        self.Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

    @contextmanager
    def get_session(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Session rollback because of: {e}")
            raise
        finally:
            session.close()

    def reload(self):
        try:
            Base.metadata.create_all(self.__engine)
            logging.info('Database reloaded successfully')
        except Exception as e:
            logging.error(f'An error occurred while reloading: {e}')

    def new(self, obj):
        try:
            with self.get_session() as session:
                session.add(obj)
                logging.info(f'New object added: {obj}')
        except Exception as e:
            logging.error(f'An error occurred while adding new object: {e}')

    def save(self):
        try:
            with self.get_session() as session:
                session.commit()
                logging.info('Session committed successfully')
        except Exception as e:
            logging.error(f'An error occurred while saving the session: {e}')

    def delete(self, obj=None):
        try:
            with self.get_session() as session:
                session.delete(obj)
                logging.info(f'{obj.__class__.__name__} deleted: {obj}')
        except Exception as e:
            logging.error(f'An error occurred while deleting object: {e}')

    def get(self, cls, **kwargs):
        try:
            with self.get_session() as session:
                filters = [getattr(cls, key) == value for key, value in kwargs.items()]
                result = session.query(cls).filter(*filters).first()
                logging.info(f'Fetched {cls.__name__}: {result}')
                return result
        except NoResultFound:
            logging.info(f'No result found for {cls.__name__} with filters: {kwargs}')
            return None
        except Exception as e:
            logging.error(f'An error occurred while fetching {cls.__name__} object: {e}')
            return None

    def get_all(self, cls, page=1, per_page=30, **kwargs):
        try:
            with self.get_session() as session:
                filters = [getattr(cls, key) == value for key, value in kwargs.items()]
                query = session.query(cls).filter(*filters)

                if cls.__name__ == 'User':
                    query = query.limit(per_page).offset((page - 1) * per_page)

                if cls.__name__ == 'Messages':
                    query = query.limit(per_page).offset((page - 1) * per_page)
                
                result = query.all()
                logging.info(f'Fetched all {cls.__name__} objects with filters: {kwargs}')
                return result
        except Exception as e:
            logging.error(f'An error occurred while fetching {cls.__name__} objects: {e}')
            return None

    def get_multiple(self, cls, ids):
        try:
            with self.get_session() as session:
                if cls == User_profile or cls == Upload:
                    result = session.query(cls).filter(cls.user_id.in_(ids)).all()
                else:
                    result = session.query(cls).filter(cls.id.in_(ids)).all()
                logging.info(f'Fetched multiple {cls.__name__} objects with IDs: {ids}')
                return result
        except Exception as e:
            logging.error(f'An error occurred while fetching multiple {cls.__name__} objects: {e}')
            return []

    def check_existing_profile(self, user_id, username=None, mobile_no=None):
        try:
            with self.get_session() as session:
                query = session.query(User_profile).filter(
                    (User_profile.user_id == user_id) |
                    (User_profile.mobile_no == mobile_no)
                )
                if username:
                    query = query.filter(User_profile.username == username)

                result = query.first()
                logging.info(f'Checked existing profile: {result}')
                return result
        except Exception as e:
            logging.error(f'An error occurred while checking profile: {e}')
            return None

    def delete_and_create_table(self, table_name: str):
        try:
            with self.get_session() as session:
                table = Table(table_name, Base.metadata, autoload_with=self.__engine)
                table.drop(self.__engine)
                Base.metadata.create_all(self.__engine)
                logging.info(f'Table {table_name} deleted and recreated successfully')
        except Exception as e:
            logging.error(f'An error occurred while deleting table {table_name}: {e}')

    def close(self):
        self.Session.remove()
        self.__engine.dispose()
