from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from services.geo_location import GeoLocation

geo_location = GeoLocation()
geo_bp = Blueprint('geo', __name__, url_prefix="/api/v1/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@geo_bp.route('/geo_location', methods=['POST'], strict_slashes=False)
@jwt_required()
def geo_route():
    data = request.json 
    response = geo_location.geo_location(data)
    return response 

@geo_bp.route('/admin/users/locations', methods=['GET'], strict_slashes=False)
def get_locations():
    response = geo_location.get_location()
    return response 