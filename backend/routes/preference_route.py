from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from controllers.preference import Preferences

preferences = Preferences()

preference_bp = Blueprint('preference', __name__, url_prefix="/v1/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@preference_bp.route('/preferences', methods=["POST"], strict_slashes=False)
@jwt_required()
def create_preference():
    try:
        # Log incoming request
        logger.info("Incoming request data: %s", request.json)
        
        # Call the controller to handle the creation logic
        response, status_code = preferences.create_preference()
        return response, status_code
    except Exception as e:
        logger.exception("Internal server error")
        return jsonify({"message": "Internal server error"}), 500
    
@preference_bp.route('/preference', methods=['GET'], strict_slashes=False)
@jwt_required()
def show_preference():
    response, status_code = preferences.show_preference()
    print(response, status_code)
    return response, status_code

@preference_bp.route('/preferences', methods=['PATCH'], strict_slashes=False)
@jwt_required()
def patch_preference():
    data = request.json 
    response, status_code = preferences.patch_preferences(data)
    return response, status_code

