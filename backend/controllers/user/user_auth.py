#!/usr/bin/env python3
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify
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

""" 
Handles user authentication
"""
class User_auth:
    def __init__(self):
        self.storage = DbStorage()

    def register_by_email(self, data):
        password = data.get('password')
        email = data.get('email')
        if is_valid_email_format(email) is False:
            return jsonify('invalid email format'), 400

        if not password or not email:
            return jsonify({'error': 'Username, password, and email are required'}), 400
        try:
            # Check if email already exist
            if self.storage.get(User, email=email):
                return jsonify({'error': 'Email already exists'}), 400
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

            # Create the user
            new_user = User(
                id=str(uuid.uuid4()),
                email=email,
                password=hashed_password.decode('utf-8')
            )
            access_token = create_access_token(identity=new_user.id)

            if not new_user:
                return jsonify({'error': 'did not create user'})
            # Save the user to the database
            self.storage.new(new_user)
            self.storage.save()
            print('user has been registered')
            print(type(new_user))
            return jsonify({'message' :'user has been registerd'}), 200
        except Exception as e:
            # Log the error
            print(f'Error during registration: {e}')
            return jsonify({'error': 'An error occurred during registration'}), 500

    def user_login(self, data):
        email = data['email']
        password = data['password']

        try:
            existing_user = self.storage.get(User, email=email)
            # check if user exists in the db
            if existing_user is None:
                return jsonify(message="User not found")

            # verify password
            encoded_pwd = password.encode('utf-8')
            result = bcrypt.checkpw(encoded_pwd, existing_user.password.encode('utf-8'))
            if result is False:
                return jsonify(message='wrong password or email')

            # create access token
            access_token = create_access_token(identity=existing_user.id)
            if isinstance(access_token, str):
                return jsonify({"access_token": access_token}), 200
            return access_token
        except Exception as e:
            print(e)
            return jsonify(message="An error occured while trying to login "), 501

if __name__ == '__main__':
    pass 