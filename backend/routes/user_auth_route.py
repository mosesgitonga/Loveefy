from flask import Flask, Blueprint, request, jsonify, request
from flask_jwt_extended import jwt_required
import os
import sys 
current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from controllers.user.user_auth import User_auth

user_auth = User_auth()

auth_bp = Blueprint('auth', __name__, url_prefix='/v1/auth')

    
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
