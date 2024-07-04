#!/usr/bin/env python3
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from controllers.recommender.rule_based import Recommender
import logging

logging.basicConfig(level=logging.INFO)

recommender = Recommender()
recommender_bp = Blueprint('recommend', __name__, url_prefix='/api/v1/')

@recommender_bp.route('/recommend', methods=['POST'], strict_slashes=False)
@jwt_required()
def recommend():
    try:
        return recommender.recommend_users()  # Directly return the response object
    except Exception as e:
        print(e) 
        return jsonify({"message": "Internal Server Error"}), 500

@recommender_bp.route('/recommendations', methods=['GET'], strict_slashes=False)
@jwt_required()
def fetch_recommendation():
    try:
        auth_header = request.headers.get('Authorization')
        logging.info(f"Authorization header: {auth_header}")

        current_user_id = get_jwt_identity()
        logging.info(f"Current user ID: {current_user_id}")
        recommendations = recommender.fetch_recommendations()
        logging.info(recommendations)
        return recommendations
    except Exception as e:
        print(e)
        return jsonify({"message": "internal Server Error"})
    