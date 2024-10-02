#!/usr/bin/env python3
from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.matches.likes import LikesService

likes_bp = Blueprint('likes', __name__, url_prefix='/api/v1/')


@likes_bp.route('/likes', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_like():
    try:
        response = LikesService().create_likes()
        return response 
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal Server Error"}), 501
    
@likes_bp.route('like-back', methods=['POST'], strict_slashes=False)
@jwt_required()
def likeback():
    try:
        response = LikesService().likeback()
    except Exception as e:
        print(e)
        return jsonify({"messages": "Internal Server Error"})
    
@likes_bp.route('reject', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def reject():
    data = request.json
    response = LikesService().reject(data)
    return response 

@likes_bp.route('notification_count', methods=['GET'], strict_slashes=False)
@jwt_required()
def notification_count():
    response = LikesService().count_notifications()
    return response