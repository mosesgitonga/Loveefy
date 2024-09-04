#!/usr/bin/env python3
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify, current_app, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
from datetime import datetime, timedelta
import os
import bcrypt
import uuid
import sys
import re
import logging
import random 
import string
import redis 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.user import User, Otp

# Initialize Limiter for rate limiting
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

storage = DbStorage()

mail = Mail()

# def is_valid_email_format(email):
#     """Verify email format using regex."""
#     email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#     return bool(re.match(email_regex, email))

class User_auth: 
    def __init__(self, mail=mail):
        self.storage = storage  
        self.created_at = datetime.now()
        self.mail = mail
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)        
        print('redis client  :  \n',self.redis_client)

    def register_by_email(self, data):
        """Register a new user by email."""
        password = data.get('password')
        email = data.get('email')
        username = data.get('username')
        
        # if not is_valid_email_format(email):
        #     return jsonify({'error': 'Invalid email format'}), 400

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
            return jsonify(error="An error occurred during login"), 500
        
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
    
    def generate_otp(self, email):
        """Generate a 6-digit OTP."""
        try:
            otp = ''.join(random.choices(string.digits, k=6))
            print('Generated OTP:', otp)
            expiration_time = 15 * 60  # OTP expires in 15 minutes

            # Store OTP in Redis
            otp_obj = self.redis_client.setex(f"otp:{email}", expiration_time, otp)
            if otp_obj is None:
                logging.error("Failed to store OTP in Redis")
                return jsonify({'message': 'Unable to store the OTP in Redis'}), 500
            
            logging.info('OTP stored in Redis successfully')
            return otp

        except Exception as e:
            logging.error(f'Error generating OTP: {e}')
            return jsonify({"message": "Internal Server Error"}), 500
        

    def verify_otp(self, data):
        try:
            otp = data.get('otp')
            email = data.get('email')

            if not otp:
                return jsonify({"message": "No OTP provided"}), 400

            if not email:
                return jsonify({"message": "No email provided"}), 400

            # Retrieve OTP from Redis
            stored_otp = self.redis_client.get(f'otp:{email}')
            if stored_otp is None:
                return jsonify({"message": "No OTP has been generated or it has expired"}), 401

            # Check if stored_otp is bytes or string and decode if needed
            if isinstance(stored_otp, bytes):
                stored_otp = stored_otp.decode('utf-8')

            if stored_otp != otp:
                return jsonify({"message": "Access Denied - Wrong OTP"}), 403

            return jsonify({"message": "Access Granted - You may change your password"}), 200

        except Exception as e:
            logging.error(f'Error verifying OTP: {e}')
            return jsonify({"error": "Internal Server Error"}), 500


            
    def send_otp_via_email(self, user):
        try:
            # Generate OTP
            otp = self.generate_otp(user.email)
            if otp is None:
                return jsonify({'message': 'Internal Server Error'}), 500
            
            print('Sending OTP:', otp)
            msg = Message(subject="Password Reset Request",
                        recipients=[user.email],
                        body=f'Dear {user.username}, \nHere is your OTP: {otp}')
            
            # Send email
            send_response = self.mail.send(msg)
            print('send response', send_response)
            if send_response is None:
                logging.error('email sent')
                return jsonify({"message": f" OTP(One Time Password) has been sent to your email: {user.email}"}), 200
            
            print('Send response:', send_response)
            return jsonify({"error": "Something went wrong"}), 500

        except Exception as e:
            logging.error(f'Error sending reset email: {e}')
            return jsonify({'error': 'Internal Server Error'}), 500
        
    def update_password(self, data):
        new_password = data.get('newPassword')
        email = data.get('email')
        
        try:
            # Fetch user by email
            user = self.storage.get(User, email=email)
            if user is None:
                logging.info('User not found')
                return jsonify({"error": "User not found"}), 404

            # Decode user password from the database
            
            hashed_password = user.password.encode('utf-8')

            # Compare the new password with the hashed password
            if bcrypt.checkpw(new_password.encode('utf-8'), hashed_password):
                return jsonify({"error": "Your old password cannot be your new password"}), 400

            # Hash the new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            # Update the user's password with the new hashed password
            user.password = hashed_password
            self.storage.new(user)
            self.storage.save()  # Assuming this method commits the changes to the database

            return jsonify({"message": "Password updated successfully"}), 200

        except Exception as e:
            logging.error(f'Error updating password: {e}')
            return jsonify({"error": "Internal Server Error"}), 500
if __name__ == '__main__':
    pass
