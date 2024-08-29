#!/usr/bin/env python3
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify, current_app
from datetime import datetime
import os
import bcrypt
import uuid
import sys
import re
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.user import User

# Initialize Limiter for rate limiting
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

storage = DbStorage()

def is_valid_email_format(email):
    """Verify email format using regex."""
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(email_regex, email))

class User_auth: 
    def __init__(self):
        self.storage = storage  # Avoid re-instantiating DbStorage
        self.created_at = datetime.now()

    def register_by_email(self, data):
        """Register a new user by email."""
        password = data.get('password')
        email = data.get('email')
        username = data.get('username')
        
        if not is_valid_email_format(email):
            return jsonify({'error': 'Invalid email format'}), 400

        if not password or not email or not username:
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

            # Save the user to the database
            self.storage.new(new_user)
            self.storage.save()

            # Generate JWT token
            access_token = create_access_token(identity=new_user.id)

            logging.info('User has been registered successfully')
            return jsonify({'message': 'User registered successfully', 'access_token': access_token}), 201

        except Exception as e:
            logging.error(f'Error during registration: {e}')
            return jsonify({'error': 'An error occurred during registration'}), 500

    @limiter.limit("5 per minute")
    def user_login(self, email, password):
        """Authenticate user and provide access token."""
        try:
            existing_user = self.storage.get(User, email=email)
            if not existing_user:
                return jsonify(message="User not found"), 404

            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), existing_user.password.encode('utf-8')):
                return jsonify(message='Wrong password or email'), 403

            # Create access token
            access_token = create_access_token(identity=existing_user.id)
            return jsonify({
                "access_token": access_token,
                "place_id": existing_user.place_id, 
                "preference_id": existing_user.preference_id,
                "current_user_id": existing_user.id,
                "current_username": existing_user.username
            }), 200

        except Exception as e:
            logging.error(f'Error during login: {e}')
            return jsonify(message="An error occurred during login"), 500
        
    @jwt_required()
    def get_user(self):
        """Retrieve the currently authenticated user's details."""
        user_id = get_jwt_identity()
        user = self.storage.get(User, id=user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_details = {
            "username": user.username,
            "email": user.email
        }
        return jsonify(user_details), 200

if __name__ == '__main__':
    pass
