from flask import Flask, Blueprint, redirect, url_for, request, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import sys 
current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.user_profile import User_profile
from controllers.user.profile import Profile

profile = Profile()
storage = DbStorage

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')

@profile_bp.route('/create', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_profile():
    try:
        data = request.get_json()
        print(data)
        response = profile.create_profile(data)
        print(response)
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@profile_bp.route('/delete/<id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_profile(id):
    try:
        profile.delete_profile(id)
        print('profile deleted')
        return jsonify({"message": "profile deleted successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@profile_bp.route('update_username', methods=['POST'], strict_slashes=False)
@jwt_required()
def update_username():
    try:
        data  = request.get_json()
        if data['username']:
            response = profile.update_username(data)
            return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"})

@profile_bp.route('update_gender', methods=['POST'], strict_slashes=False)
@jwt_required()
def update_gender():
    try:
        data = request.get_json()
        response = profile.update_gender(data)
        return response
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"})
    
#@profile_bp.route('update_age', methods=['POST'], strict_slashes=False)
#@jwt_required