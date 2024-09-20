from flask import Flask, Blueprint, request, jsonify, request
from flask_jwt_extended import jwt_required
import os
import sys 
import logging
import bcrypt
current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from controllers.user.user_auth import User_auth
from models.engine.DBStorage import DbStorage
from models.user import User 

user_auth = User_auth()
storage = DbStorage()
auth_bp = Blueprint('auth', __name__, url_prefix='/v1/auth')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@auth_bp.route('/registers/', methods=['POST'], strict_slashes=False)
def register():
    try:
        data = request.get_json()
        if not data:
            print('no data')
            return jsonify({'no data retrieved'})
        registration_response = user_auth.register_by_email(data)
        if registration_response is not None:
            return registration_response
        print('an error occured while registering user')            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/logins', methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json() 
    access_token = user_auth.user_login(data.get('email'), data.get('password'))
    if isinstance(access_token, str):
        return jsonify({"access_token": {access_token}}), 200
    return access_token

@auth_bp.route('/reset_password_request', methods=['POST'], strict_slashes=False)
def reset_password_request():
    data = request.json
    email = data.get('email')
    logging.info(email)
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = storage.get(User, email=email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        res = user_auth.send_otp_via_email(user)
        return res
    except Exception as e:
        logging.error(f'Error sending reset email: {e}')
        return jsonify({'error': 'Failed to send reset email'}), 500
    
@auth_bp.route('/reset_password/<token>', methods=['POST'], strict_slashes=False)
def reset_password(token):
    try:
        email = user_auth.verify_reset_token(token)
        if not email:
            return jsonify({'error': 'Invalid or expired token'}), 400

        data = request.json
        new_password = data.get('password')
        if not new_password:
            return jsonify({'error': 'Password is required'}), 400

        # Retrieve the user and update their password
        user = storage.get(User, email=email)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(10))
        user.password = hashed_password.decode('utf-8')

        # Save the updated user information
        storage.save()

        return jsonify({'message': 'Password has been reset successfully'}), 200

    except Exception as e:
        logging.error(f'Error during password reset: {e}')
        return jsonify({'error': 'Failed to reset password'}), 500

@auth_bp.route('/update_password', methods=['PATCH'], strict_slashes=False)
def update_password():
    data = request.json 

    otp_verification_response, otp_status_code = user_auth.verify_otp(data)
    if otp_status_code != 200:
        return otp_verification_response

    password_update_response = user_auth.update_password(data)
    return password_update_response

@auth_bp.route('/account/delete', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_account():
    response, status_code = user_auth.delete_account()
    return response, status_code
