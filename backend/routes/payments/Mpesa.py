from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from services.payments.mpesa import Mpesa
mpesa = Mpesa()

mpesa_bp = Blueprint('mpesa', __name__, url_prefix="/api/mpesa/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@mpesa_bp.route('/stk-push', methods=['POST'], strict_slashes=False)
@jwt_required()
def mpesa_express():
    response = mpesa.stk_push()
    return response 

@mpesa_bp.route('/callback', methods=['POST'])
def callback():
    data = request.json
    print("Callback received:", data)
    return jsonify({"status": "success"})