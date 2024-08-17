#!/usr/bin/env python3
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify
from datetime import datetime
import os
import random
import bcrypt
import uuid
import sys
import re
import logging


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
        self.created_at = datetime.now()

    def register_by_email(self, data):
        password = data.get('password')
        email = data.get('email')
        username = data.get('username')
        res = is_valid_email_format(email)
        if res is False:
            return jsonify({'error': 'Invalid email format'}), 400

        if not password or not email:
            return jsonify({'error': 'Username, password, and email are required'}), 400
        try:
            # Check if email already exists
            if self.storage.get(User, email=email):
                return jsonify({'error': 'Email already exists', 'code': 600}), 409

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

            # Create the user
            new_user = User(
                id=str(uuid.uuid4()),
                created_at=self.created_at,
                email=email,
                password=hashed_password.decode('utf-8'),
                username=username
            )

            if not new_user:
                return jsonify({'error': 'Did not create user'}), 500

            # Save the user to the database
            self.storage.new(new_user)
            self.storage.save()
            access_token = create_access_token(identity=new_user.id)

            logging.info('User has been registered')
            logging.info(type(new_user))
            return jsonify({'message': 'User has been registered', 'access_token': access_token}), 201
        except Exception as e:
            # Log the error
            logging.error(f'Error during registration: {e}')
            return jsonify({'error': 'An error occurred during registration'}), 500

    def user_login(self, email, password):
        try:

            existing_user = self.storage.get(User, email=email)
            # check if user exists in the db
            if existing_user is None:
                return jsonify(message="User not found"), 404

            # verify password
            encoded_pwd = password.encode('utf-8')
            result = bcrypt.checkpw(encoded_pwd, existing_user.password.encode('utf-8'))
            if result is False:
                return jsonify(message='wrong password or email'), 403

            # create access token
            access_token = create_access_token(identity=existing_user.id)
            if isinstance(access_token, str):
                print(existing_user.place_id)
                return jsonify({
                    "access_token": access_token,
                    "place_id": existing_user.place_id, 
                    "preference_id": existing_user.preference_id,
                    "current_user_id": existing_user.id,
                    "current_username": existing_user.username}), 200
                
            return access_token
        except Exception as e:
            print(e)
            return jsonify(message="An error occured while trying to login "), 501

if __name__ == '__main__':
    pass 
