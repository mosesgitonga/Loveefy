from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from services.message import MessageService

messages = MessageService()
messages_bp = Blueprint('message', __name__, url_prefix="/api/v1/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@messages_bp.route('/rooms', methods=['GET'], strict_slashes=False)
@jwt_required()
def list_rooms():
    try:
        res = messages.list_rooms()
        return res  # Return the response directly if it's already JSON formatted
    except Exception as e:
        logger.error(f"Error listing rooms for user {get_jwt_identity()}: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
