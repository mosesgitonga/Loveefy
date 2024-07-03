#!/usr/bin/env python3
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from controllers.recommender.rule_based import Recommender

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
        return recommender.fetch_recommendations()
    except Exception as e:
        print(e)
        return jsonify({"message": "internal Server Error"})
    