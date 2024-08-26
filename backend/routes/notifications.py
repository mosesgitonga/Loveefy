from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from controllers.matches.likes import LikesService
likesService= LikesService()

notifications_bp = Blueprint('notifications', __name__, url_prefix="/api/v1/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@notifications_bp.route('/notifications', methods=['GET'], strict_slashes=False)
@jwt_required()
def notify():
    try:
        response = likesService.list_notifications()
        return response 
    except Exception as e:
        logger.info(e)
        return jsonify({"message": "Internal Server Error"})