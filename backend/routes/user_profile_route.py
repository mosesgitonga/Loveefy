from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from controllers.user.profile import Profile
from controllers.place.place_control import Place_control
from controllers.preference import Preferences


profile_bp = Blueprint('profile', __name__, url_prefix='/v1/')
profile = Profile()
place = Place_control()
preferences = Preferences()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@profile_bp.route('/profiles', methods=['POST'], strict_slashes=False)
@jwt_required()
def creates_profile():
    try:
        profile_data = request.get_json()
        if not profile_data:
            return jsonify({"message": "No data provided"}), 400

        # Create profile

        profile_response = profile.create_profile(profile_data)
        
        # If all creations are successful
        return jsonify({"message": "Profile and place created successfully"}), 201
        
    except Exception as e:
        logger.error(f"Exception: {e}")
        return jsonify({"message": "Internal server error"}), 500

@profile_bp.route('/profiles/delete/<id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_profile(id):
    try:
        profile.delete_profile(id)  # Assuming delete_profile method exists in Profile
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
            return jsonify(response), 200  # Assuming update_username returns a dictionary

        return jsonify({"message": "Username not provided"}), 400

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

@profile_bp.route('/profiles/update_gender', methods=['POST'], strict_slashes=False)
@jwt_required()
def update_gender():
    try:
        data = request.get_json()
        response = profile.update_gender(data)  # Assuming update_gender method exists in Profile
        return jsonify(response), 200  # Assuming update_gender returns a dictionary

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
