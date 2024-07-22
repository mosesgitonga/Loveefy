#!/usr/bin/env python3
from flask import Blueprint
from flask import jsonify
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