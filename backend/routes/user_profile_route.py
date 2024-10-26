from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Api, Resource, fields, Namespace
import logging

from controllers.user.profile import Profile
from controllers.place.place_control import Place_control
from controllers.preference import Preferences
from controllers.user.user_auth import User_auth

# Setup Blueprint and Namespace
profile_bp = Blueprint('profile', __name__, url_prefix='/api/v1/')
profile_api = Namespace('api/v1/', description="API for user's Profile")

profile = Profile()
place = Place_control()
preferences = Preferences()
user = User_auth()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

profile_model = profile_api.model("ProfileFormModel",
    {"country": fields.String(required=True, description="user country"),
    "region": fields.String(required=True, description="user region"),
    "sub_region": fields.String(required=True, description="sub region"),
    "gender": fields.String(required=True, description="user gender"),
    "dob": fields.String(required=True, description="date of birth (%Y-%m-%d)"),
    "mobile_no": fields.String(required=True, description="mobile no"),
    "industry_major": fields.String(required=True, description="Industry Major, eg: Health, Information Technology"),
    "education_level": fields.String(required=True, description="education level"),
    "career": fields.String(required=True, description="career eg: Doctor"),
    "employment": fields.String(required=True, description="Employment eg: employed, self employed, unemployed"),
    "is_schooling": fields.String(required=True, description="is schooling"),
    "has_child": fields.String(required=True, description="does user have a child")}
)

update_fields_model = profile_api.model("UpdateFields", {
                'username': fields.String(required=False, description="username"),
                'gender': fields.String(required=False, description="gender"),
                'country': fields.String(required=False, description="country"),
                'industry_major': fields.String(required=False, description="Industry"),
                'education_level': fields.String(required=False, description="Education level"),
                'career': fields.String(required=False, description="career"),
                'dob': fields.String(required=False, description="date of birth (%Y-%m-%d)"),
                'region': fields.String(required=False),
                'sub_region': fields.String(required=False),
                'mobile_no': fields.String(required=False),
                'subscription_type': fields.String(required=False)
            })
# Helper function for JSON validation
def get_json_data():
    if request.content_type != 'application/json':
        return None, {"message": "Content-Type must be application/json"}, 400
    data = request.get_json()
    if not data:
        return None, {"message": "No data provided"}, 400
    return data, None, None

@profile_api.route('/profiles')
class ProfileResource(Resource):
    @jwt_required()
    @profile_api.expect(profile_model)
    def post(self):
        try:
            profile_data, error_response, status_code = get_json_data()
            if error_response:
                return jsonify(error_response), status_code
            logger.info('Profile data: %s', profile_data)
            profile_response = profile.create_profile(profile_data)
            return jsonify(profile_response)
        except Exception as e:
            logger.error(f"Exception: {e}")
            return jsonify({"message": "Internal server error"}), 500

@profile_api.route('/profiles/update', strict_slashes=False)
class ProfileUpdateResource(Resource):
    @jwt_required()
    @profile_api.expect(update_fields_model)
    def patch(self):
        try:
            data, error_response, status_code = get_json_data()
            if error_response:
                return jsonify(error_response), status_code

            response = profile.update_fields(data)
            return response 

        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            return jsonify({"message": "Internal Server Error"}), 500

# @profile_api.route('/profiles/username', strict_slashes=False)
# class UpdateUsernameResource(Resource):
#     @jwt_required()
#     def patch(self):
#         try:
#             data, error_response, status_code = get_json_data()
#             if error_response:
#                 return jsonify(error_response), status_code

#             if 'username' not in data:
#                 return jsonify({"message": "Username not provided"}), 400

#             response = profile.update_username(data)
#             return jsonify(response), 200

#         except Exception as e:
#             logger.error(f"Error updating username: {e}")
#             return jsonify({"message": "Internal server error"}), 500

# @profile_api.route('/profiles/gender', strict_slashes=False)
# class UpdateGenderResource(Resource):
#     @jwt_required()
#     def patch(self):
#         try:
#             data, error_response, status_code = get_json_data()
#             if error_response:
#                 return jsonify(error_response), status_code

#             response = profile.update_gender(data)
#             return jsonify(response), 200

#         except Exception as e:
#             logger.error(f"Error updating gender: {e}")
#             return jsonify({"message": "Internal server error"}), 500

# Delete profile by ID
# @profile_api.route('/profiles/<id>', methods=['DELETE'], strict_slashes=False)
# class DeleteProfileResource(Resource):
#     @jwt_required()
#     def delete(self, id):
#         try:
#             profile.delete_profile(id)
#             return jsonify({"message": "Profile deleted successfully"}), 200

#         except Exception as e:
#             logger.error(f"Error deleting profile {id}: {e}")
#             return jsonify({"message": "Internal server error"}), 500
