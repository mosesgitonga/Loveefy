from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from controllers.user.profile import Profile
from controllers.place.place_control import Place_control
from controllers.preference import Preferences
from controllers.user.user_auth import User_auth


profile_bp = Blueprint('profile', __name__, url_prefix='/api/v1/')
profile = Profile()
place = Place_control()
preferences = Preferences()
user = User_auth()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@profile_bp.route('/profiles', methods=['POST'], strict_slashes=False)
@jwt_required()
def creates_profile():
    try:
        # Ensure the content type is application/json
        if request.content_type != 'application/json':
            return jsonify({"message": "Content-Type must be application/json"}), 400
        
        profile_data = request.get_json()
        logger.info('Profile data: %s', profile_data)  # Use a placeholder for logging
        
        if not profile_data:
            return jsonify({"message": "No data provided"}), 400

        # Create profile
        profile_response = profile.create_profile(profile_data)

        # If creation is successful
        return jsonify({"message": "Profile created successfully"}), 201

    except Exception as e:
        logger.error(f"Exception: {e}")
        return jsonify({"message": "Internal server error"}), 500

# @profile_bp.route('/profile', methods=['GET'], strict_slashes=False)
# @jwt_required()
# def get_profile():
#     profile_response = profile.get_profile()
#     user_response = user.get_user()
#     user_data = {
#         "username": user_response['username'],
#         "industry_major": profile_response['industry_major'],
#         "career": profile_response['career'],
#         "dob": profile_response['dob']
#     }
#     return jsonify(user_data)

@profile_bp.route('/profiles/update', methods=['PATCH'], strict_slashes=False)
@jwt_required()
def update():
    try:
        data = request.get_json()

        profile.update_fields(data)

        return jsonify({'message': "updated successfully"})
    except Exception as e:
        logger.error(e)
        return jsonify({"message": "Internal Server Error"})

@profile_bp.route('/profiles/delete/<id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_profile(id):
    try:
        profile.delete_profile(id)  
        return jsonify({"message": "Profile deleted successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

@profile_bp.route('/profiles/update', methods=['POST'], strict_slashes=False)
@jwt_required()
def update_username():
    try:
        data = request.get_json()
        if 'username' in data:
            response = profile.update_username(data)
            return jsonify(response), 200 

        return jsonify({"message": "Username not provided"}), 400

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

@profile_bp.route('/profiles/update_gender', methods=['POST'], strict_slashes=False)
@jwt_required()
def update_gender():
    try:
        data = request.get_json()
        response = profile.update_gender(data)  
        return jsonify(response), 200  

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
    
@profile_bp.route('/profile/<userId>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user_profile(userId):
    
    response = profile.get_profile(userId)
    return response
