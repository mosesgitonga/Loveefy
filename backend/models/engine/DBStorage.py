from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from models.base_model import Base
from models.user import User
from models.user_profile import User_profile
from dotenv import load_dotenv
import os

load_dotenv()


class DbStorage:
    __engine = None
    __session = None

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
        self.__session = self.Session()

    def reload(self):
        """Reloads data from the database and refreshes session."""
        try:
            Base.metadata.create_all(self.__engine)
            self.__session = self.Session()
            print('Database reloaded successfully')
        except Exception as e:
            print(f'An Error occurred while reloading: {e}')

    def new(self, obj):
        """Adds a new object to the current session."""
        self.__session.add(obj)

    def save(self):
        """Commits changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes the specified object from the database."""
        if obj:
            self.__session.delete(obj)

    def get(self, cls=None, **kwargs):
        """Fetches an object from the database based on the provided class and filters."""
        if not cls:
            return None

        try:
            filters = []
            for key, value in kwargs.items():
                attr = getattr(cls, key, None)
                if attr is not None:
                    filters.append(attr == value)
            if filters:
                return self.__session.query(cls).filter(*filters).first()
            else:
                raise ValueError('Invalid arguments provided for get method')
        except NoResultFound:
            return None
        except ValueError as ve:
            print(ve)
            return None
        except Exception as e:
            print(f'An Error occurred while fetching {cls.__name__} object: {e}')
            return None

    def get_all(self, cls=None, **kwargs):
        """Fetches all objects from the database based on the provided class and filters.
            Return -> returns all objects except the objects containing the filters
        """
        if not cls:
            return None

        try:
            batch_size = 50
            offset = 0
            all_profiles = []
            
            filters = []

            # Prepare filters
            for key, value in kwargs.items():
                attr = getattr(cls, key, None)
                if attr is not None:
                    if isinstance(value, list):
                        filters.append(attr.notin_(value))
                    else:
                        filters.append(attr != value)

            # Fetch profiles in batches
            if filters:
                while True:
                    profiles_batch = self.__session.query(cls) \
                        .filter(*filters) \
                        .limit(batch_size) \
                        .offset(offset) \
                        .all()

                    if not profiles_batch:
                        break

                    all_profiles.extend(profiles_batch)
                    offset += batch_size

            else:
                raise ValueError('Invalid arguments provided for get_all method')

            return all_profiles

        except ValueError as ve:
            print(ve)
            return None
        except Exception as e:
            print(f'An Error occurred while fetching {cls.__name__} objects: {e}')
            return None
    

    def check_existing_profile(self, user_id, username=None, mobile_no=None):
        """Checks if a profile with the given criteria exists."""
        try:
            query = self.__session.query(User_profile).filter(
                (User_profile.user_id == user_id) |
                (User_profile.mobile_no == mobile_no)
            )
            if username:
                query = query.filter(User_profile.username == username)

            return query.first()
        except Exception as e:
            print(f'An error occurred while checking profile: {e}')
            return None

    def close(self):
        """Closes the session and disposes the engine."""
        self.__session.close()
        self.__engine.dispose()

if __name__ == "__main__":
    storage = DbStorage()
    # Example usage:
    user = storage.get(User, username='john_doe')
    if user:
        print(f'User found: {user.username}')
    else:
        print('User not found or error occurred.')

    # Remember to close the session and dispose the engine when done
    storage.close()
