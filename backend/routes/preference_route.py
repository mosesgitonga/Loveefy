from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required
from flask_restx import Api, Resource, fields, Namespace
import logging

from controllers.preference import Preferences

preferences = Preferences()

# Define the API namespace
preference_api = Namespace('api/v1/', description="User preference API endpoints")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define models
preference_model = preference_api.model('Preference', {
    'gender': fields.String(required=True, description='Preferred gender, e.g., male/female'),
    'minAge': fields.String(required=True, description='Preferred minimum age'),
    'maxAge': fields.String(required=True, description='Preferred maximum age'),
    'country': fields.String(required=True, description='Preferred country'),
    'region': fields.String(required=True, description='Preferred region within the country'),
    'industry_major': fields.String(required=True, description='Preferred industry major'),
    'career': fields.String(required=True, description='Preferred partner career'),
    'education_level': fields.String(required=True, description='Preferred partner education level'),
    'employment': fields.String(required=True, description='Preferred partner employment status'),
    'is_schooling': fields.String(required=True, description='Does user prefer partner who is schooling? (yes/no/any)'),
    'fav_hobby': fields.String(required=True, description='Preferred partner hobby'),
    'wants_child': fields.String(required=True, description='Does user prefer partner with children? (yes/no/any)'),
})

# Model for updating preferences (optional fields)
preference_model_update = preference_api.model('PreferenceUpdate', {
    'gender': fields.String(required=False, description='Preferred gender, e.g., male/female'),
    'minAge': fields.String(required=False, description='Preferred minimum age'),
    'maxAge': fields.String(required=False, description='Preferred maximum age'),
    'country': fields.String(required=False, description='Preferred country'),
    'region': fields.String(required=False, description='Preferred region within the country'),
    'industry_major': fields.String(required=False, description='Preferred industry major'),
    'career': fields.String(required=False, description='Preferred partner career'),
    'education_level': fields.String(required=False, description='Preferred partner education level'),
    'employment': fields.String(required=False, description='Preferred partner employment status'),
    'is_schooling': fields.String(required=False, description='Does user prefer partner who is schooling? (yes/no/any)'),
    'fav_hobby': fields.String(required=False, description='Preferred partner hobby'),
    'wants_child': fields.String(required=False, description='Does user prefer partner with children? (yes/no/any)'),
})

# Routes
@preference_api.route('/preference')
class PreferenceResource(Resource):
    
    @jwt_required()
    @preference_api.expect(preference_model)
    def post(self):
        """Create a new user preference"""
        try:
            logger.debug("Incoming request data: %s", request.json)
            response = preferences.create_preference()
            return jsonify(response)
        except Exception as e:
            logger.exception("Internal server error")
            return jsonify({"message": "Internal server error"}), 500
    
    @jwt_required()
    def get(self):
        """Show user preferences"""
        try:
            response, status_code = preferences.show_preference()
            return response, status_code
        except Exception as e:
            logger.exception("Internal server error")
            return jsonify({"message": "Internal server error"}), 500

    @jwt_required()
    @preference_api.expect(preference_model_update)  # Expect update model for patch
    def patch(self):
        """Update user preferences"""
        try:
            data = request.json
            response, status_code = preferences.patch_preferences(data)
            return response, status_code
        except Exception as e:
            logger.exception("Internal server error")
            return jsonify({"message": "Internal server error"}), 500
