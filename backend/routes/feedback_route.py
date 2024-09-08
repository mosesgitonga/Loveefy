from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from controllers.feedback import FeedbackHandler

feedback = FeedbackHandler()
feedback_bp = Blueprint('feedback', __name__, url_prefix="/api/v1/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@feedback_bp.route('/feedback', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_feedback():
    data = request.json 
    response = feedback.create_feedback(data)
    return response 
