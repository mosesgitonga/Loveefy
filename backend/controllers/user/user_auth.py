#!/usr/bin/env python3
import os
import random
import bcrypt
import uuid
import sys
import re

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.user import User

storage = DbStorage()

def is_valid_email_format(email):
    """verify email format"""
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_regex, email):
        print('invalid email format')
        return False
    else:
        print('valid email')

""" 
Handles user authentication
"""
class User_auth:
    def __init__(self):
        self.storage = DbStorage()

    def register_by_email(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs['password']
        email = kwargs['email']
        if is_valid_email_format(email) is False:
            return
        if not username or not password or not email:
            raise ValueError('Error: Username, password, and email are required')

        try:
            # Check if username and email already exist
            if self.storage.get(User, email=email):
                raise ValueError('Error: Email already exists')
            if self.storage.get(User, username=username):
                raise ValueError('Error: Username already exists')
            print(username)
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

            # Create the user
            new_user = User(
                id=str(uuid.uuid4()),
                username=username,
                email=email,
                password=hashed_password.decode('utf-8')
            )

            # Save the user to the database
            self.storage.new(new_user)
            self.storage.save()
            print('user has been registered')

            return new_user
        except Exception as e:
            # Log the error
            print(f'Error during registration: {e}')
            return None

if __name__ == '__main__':
    user_auth = User_auth()
    try:
        user = user_auth.register_by_email(password='123', email='andrew@axample.com', username='andrew')
    except Exception as e:
        print(e)
