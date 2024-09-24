from flask import Blueprint, jsonify
from controllers.uploads import UploadHandler
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging 

upload = UploadHandler()

upload_bp = Blueprint('upload', __name__, url_prefix="/api/v1/")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@upload_bp.route('/uploads', methods=['POST'], strict_slashes=False)
@jwt_required()
def upload_pic():
    try:
        response, status_code = upload.upload_image()
        return response, status_code
    except Exception as e:
        logger.exception("Internal server error")
        return jsonify({"message": "Internal server error"}), 500 
        
