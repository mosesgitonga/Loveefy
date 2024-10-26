from flask import Flask, Blueprint, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from flask_jwt_extended import jwt_required
import os
import sys 
import logging
import bcrypt

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from controllers.user.user_auth import User_auth, AdminAuth
from models.engine.DBStorage import DbStorage
from models.user import User 

user_auth = User_auth()
admin_auth = AdminAuth()
storage = DbStorage()

#auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
auth_api = Namespace('api/v1/auth', description="Auth")
#login_api = Namespace('login', description='login user')

#api = Namespace('login', description="login endpoints")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('auth')

user_model = auth_api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'username': fields.String(required=True, description='username required')
})

login_model = auth_api.model('Login', {
    'email': fields.String(required=True, description="User email"),
    'password': fields.String(required=True, description="User password")
})

reset_password_model = auth_api.model('Resetpassword', {
    "email": fields.String(required=True, description="user email"),
    "token": fields.String(required=True, description="token"),
    "new_password": fields.String(required=True, description="new password")
})
token_request_model = auth_api.model('TokenRequest', {
    "email": fields.String(required=True, description="user email"),
})

del_account_model = auth_api.model('DeleteAccount', {
    "password": fields.String(required=True, description='user password')
})


@auth_api.route('/registers/')
class Register(Resource):
    @auth_api.expect(user_model)
    def post(self):
        try:
            data = request.get_json()
            if not data:
                logger.error("No data retrieved in register request")
                return jsonify({'error': 'No data retrieved'}), 400
            
            registration_response = user_auth.register_by_email(data)
            if registration_response is not None:
                return registration_response
            
            logger.error("Error occurred while registering user")
            return jsonify({'error': 'Registration failed'}), 500
        except ValueError as ve:
            logger.error(f"Invalid data format: {ve}")
            return jsonify({'error': 'Invalid input format'}), 400
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({'error': str(e)}), 500

@auth_api.route('/logins')
class Login(Resource):
    @auth_api.expect(login_model)
    def post(self):
        try:
            data = request.get_json()
            if not data:
                logger.error("No data retrieved in login request")
                return jsonify({'error': 'No data retrieved'}), 400
            
            response, status_code = user_auth.user_login(data.get('email'), data.get('password'))
            return response, status_code
        except ValueError as ve:
            logger.error(f"Invalid data format: {ve}")
            return jsonify({'error': 'Invalid input format'}), 400
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({'error': str(e)}), 500

@auth_api.route('/token_request')
class ResetPasswordRequest(Resource):
    @auth_api.expect(token_request_model)
    def post(self):
        try:
            data = request.json
            email = data.get('email')
            if not email:
                logger.error("No email provided")
                return jsonify({'error': 'Email is required'}), 400

            user = storage.get(User, email=email)
            if not user:
                logger.info(f"User with email {email} not found")
                return jsonify({'error': 'User not found'}), 404

            res = user_auth.send_otp_via_email(user)
            return res
        except Exception as e:
            logger.error(f"Error sending reset email: {e}")
            return jsonify({'error': 'Failed to send reset email'}), 500

@auth_api.route('/reset_password')
class ResetPassword(Resource):
    @auth_api.expect(reset_password_model)
    def post(self):
        try:  
            data = request.json 
            response = user_auth.verify_otp(data)
            return response

        except Exception as e:
            logger.error(f"Error during password reset: {e}")
            return jsonify({'error': 'Failed to reset password'}), 500

@auth_api.route('/update_password')
class UpdatePassword(Resource):
    def post(self):
        try:
            data = request.json
            otp_verification_response, otp_status_code = user_auth.verify_otp(data)
            if otp_status_code != 200:
                return otp_verification_response

            password_update_response = user_auth.update_password(data)
            return password_update_response
        except Exception as e:
            logger.error(f"Error updating password: {e}")
            return jsonify({'error': 'Failed to update password'}), 500

@auth_api.route('/account/delete')
class DeleteAccount(Resource):
    @jwt_required()
    @auth_api.expect(del_account_model)
    def delete(self):
        try:
            data = request.json 
            response, status_code = user_auth.delete_account(data)
            return response, status_code
        except Exception as e:
            logger.error(f"Error deleting account: {e}")
            return jsonify({'error': 'Failed to delete account'}), 500

@auth_api.route('/super/admin/register')
class AdminRegister(Resource):
    def post(self):
        try:
            data = request.json
            response = admin_auth.register_super_admin(data)
            return response
        except Exception as e:
            logger.error(f"Error registering super admin: {e}")
            return jsonify({'error': 'Failed to register super admin'}), 500



@auth_api.route('/users/count')
class CountUsers(Resource):
    def get(self):
        try:
            response = user_auth.count_users_in_redis()
            return response
        except Exception as e:
            logger.error(f"Error counting users: {e}")
            return jsonify({'error': 'Failed to count users'}), 500
