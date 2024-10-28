#!/usr/bin/env python3
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify, current_app, url_for, request 
from itsdangerous import URLSafeTimedSerializer
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
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
from flask_socketio import SocketIO, emit

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.user import User, Otp
from models.place import Place
from models.uploads import Upload
from models.user_profile import User_profile
from models.recommendation import Recommendation
from models.admin import Admin, PowerLevel
from models.preference import Preference
from controllers.recommender.rule_based import Recommender


# Initialize Limiter for rate limiting
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

storage = DbStorage()

mail = Mail()
socketio = SocketIO()
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

        #self.initialize_user_count()


    def initialize_user_count(self):
        """Initialize user count in Redis if it's not already set."""
        if not self.redis_client.exists('user_count'):
            user_count = self.get_user_count()
            self.redis_client.set('user_count', user_count)
        print(f"User count initialized in Redis: {self.redis_client.get('user_count')}")

    def get_user_count(self):
        """Get the total number of users in the database."""
        all_users = len(self.storage.get_all(User))
        return all_users

    def count_users_in_redis(self):
        updated_user_count = self.redis_client.get('user_count')
        return updated_user_count
    
    def register_by_email(self, data):
        """Register a new user by email."""
        password = data.get('password')
        email = data.get('email')
        username = data.get('username')
        
        # if not is_valid_email_format(email):
        #     return jsonify({'error': 'Invalid email format'}), 400

        if not password or not email or not username:
            return {'error': 'Username, password, and email are required'}, 400

        try:
            if self.storage.get(User, email=email):
                return {'error': 'Email already exists', 'code': 600}, 409

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
            return {'message': 'User registered successfully', 'access_token': access_token}, 201

        except Exception as e:
            logging.error(f'Error during registration: {e}')
            return {'error': 'An error occurred during registration'}, 500

    @limiter.limit("5 per minute")
    def user_login(self, email, password):
        """Authenticate user and provide access token."""
        try:
            existing_user = self.storage.get(User, email=email)
            if not existing_user:
                return {"message": "User not found"}, 404

            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), existing_user.password.encode('utf-8')):
                return {"message": "Wrong password or email"}, 403

            # Create access token
            access_token = create_access_token(identity=existing_user.id)
            return {
                "access_token": access_token,
                "place_id": existing_user.place_id, 
                "preference_id": existing_user.preference_id,
                "current_user_id": existing_user.id,
                "current_username": existing_user.username
            }, 200

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
        return jsonify(user_details)
    
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
            otp = data.get('token')
            email = data.get('email')
            print('otp:', otp)

            if not otp:
                return {"message": "No OTP provided"}, 400

            if not email:
                return {"message": "No email provided"}, 400

            stored_otp = self.redis_client.get(f'otp:{email}')
            if stored_otp is None:
                return {"message": "No OTP has been generated or it has expired"}, 401

            # Check if stored_otp is bytes or string and decode if needed
            if isinstance(stored_otp, bytes):
                stored_otp = stored_otp.decode('utf-8')

            if stored_otp != otp:
                return {"message": "Access Denied - Wrong OTP"}, 403

            res = self.update_password(data)
            return res
            

        except Exception as e:
            logging.error(f'Error verifying OTP: {e}')
            return {"error": "Internal Server Error"}, 500


            
    def send_otp_via_email(self, user):
        try:
            # Generate OTP
            otp = self.generate_otp(user.email)
            if otp is None:
                return {'message': 'Internal Server Error'}, 500
            
            print('Sending OTP:', otp)
            msg = Message(subject="Password Reset Request",
                        recipients=[user.email],
                        body=f'Dear {user.username}, \nHere is your OTP: {otp}')
            
            # Send email
            send_response = self.mail.send(msg)
            print('send response', send_response)
            if send_response is None:
                logging.error('email sent')
                return {"message": f" OTP(One Time Password) has been sent to your email: {user.email}"}, 200
            
            print('Send response:', send_response)
            return {"error": "Something went wrong"}, 500

        except Exception as e:
            logging.error(f'Error sending reset email: {e}')
            return {'error': 'Internal Server Error'}, 500
        
    def update_password(self, data):
        new_password = data.get('new_password')
        email = data.get('email')

        if not new_password or not email:
            logging.error("Missing newPassword or email in request")
            return {"error": "Both email and new password are required"}, 400

        try:
            user = self.storage.get(User, email=email)
            if user is None:
                logging.info('User not found')
                return {"error": "User not found"}, 404
            
            old_hashed_password = user.password.encode('utf-8')
            new_password_encoded = new_password.encode('utf-8')

            if bcrypt.checkpw(new_password_encoded, old_hashed_password):
                return {"error": "Your old password cannot be your new password"}, 400

            hashed_password = bcrypt.hashpw(new_password_encoded, bcrypt.gensalt())

            user.password = hashed_password
            self.storage.new(user)
            self.storage.save()

            return {"message": "Password updated successfully"}, 200

        except Exception as e:
            logging.error(f'Error updating password: {e}')
            return {"error": "Internal Server Error"}, 500


        
    def delete_account(self, data):
        user_id = get_jwt_identity()
        password = data.get('password')
        try:
            user = self.storage.get(User, id=user_id)
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return {"Forbidden": "Wrong password"}, 403

            if  user:
                self.storage.delete(obj=user)
                self.storage.new(user)
                self.storage.save()

            recommender = Recommender()
            recommender.recommend_users()
            return {"message": "User Deleted Successfully"}, 200
        except Exception as e:
            print(e)
            return {"message": "Internal Server Error"}, 500
        


from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

class AdminAuth:
    def __init__(self):
        self.storage = DbStorage()
    
    def register_super_admin(self, data):
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"{field} is required to register a super admin.")

        existing_super_admin = self.storage.get(Admin, power=PowerLevel.SUPER)
        if existing_super_admin:
            return jsonify({"message": "Permission Denied"}), 403
        
        hashed_password = generate_password_hash(data['password'])
        
        # Create a new super admin
        new_super_admin = Admin(
            name=data['name'],
            email=data['email'],
            power=PowerLevel.SUPER,
            password=hashed_password
        )

        try:
            # Save to the database
            self.storage.new(new_super_admin)
            self.storage.save()
            return {"status": "success", "message": "Super admin registered successfully."}
        except IntegrityError:
            self.storage.rollback()
            return {"status": "error", "message": "Email already exists."}
        
    def admin_login(self, data):
        required_fields = ['email', 'password']
        
        for field in required_fields:
            if field not in data:
                raise BadRequest(f'{field} is required')  

        try:    
            existing_admin = self.storage.get(Admin, email=data['email'])
            
            if not existing_admin:
                return jsonify({"message": "Access Denied"}), 403
            
            password = data['password']
            if not check_password_hash(existing_admin.password, data['password']):
                return jsonify({"status": "error", "message": "Access Denied"}), 403
                
            access_token = create_access_token(identity=existing_admin.id)
            return jsonify({"access_token": access_token}), 200 

        except Exception as e:
            # Log the exception and return a generic error message
            print(f"Error during login: {e}")
            return jsonify({"error": "An error occurred during login."}), 500 
        
    
        
    

