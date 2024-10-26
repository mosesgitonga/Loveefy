#!/usr/bin/env python3
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Api, Resource, fields, Namespace
import logging
from controllers.recommender.rule_based import Recommender

logging.basicConfig(level=logging.INFO)

# Initialize Recommender and Blueprint
recommender = Recommender()
recommender_api = Namespace('api/v1/', description="Recommendation API endpoints")

# Swagger models for the responses
recommendation_model = recommender_api.model('Recommendation', {
    'user_id': fields.Integer(description='Recommended user ID'),
    'score': fields.Float(description='Recommendation score based on rules')
})

# Routes and logic
@recommender_api.route('/recommend')
class Recommend(Resource):
    @jwt_required()
    @recommender_api.doc(description="Recommend users based on specified rules\nIt can only be generated when the user profile and preferences has been created.")
    @recommender_api.response(200, 'Successful Recommendation', [recommendation_model])
    @recommender_api.response(500, 'Internal Server Error')
    def post(self):
        """
        POST /recommend
        ---
        Generates recommended users based on rule-based logic.
        """
        try:
            logging.info("Generating recommendations")
            recommendations = recommender.recommend_users()
            return jsonify(recommendations)
        except Exception as e:
            logging.error(f"Recommendation error: {e}")
            return jsonify({"message": "Internal Server Error"}), 500


@recommender_api.route('/recommendations')
class FetchRecommendation(Resource):
    @jwt_required()
    @recommender_api.doc(description="Fetch user-specific recommendations")
    @recommender_api.response(200, 'Recommendations successfully retrieved', [recommendation_model])
    @recommender_api.response(500, 'Internal Server Error')
    def get(self):
        """
        GET /recommendations
        ---
        Retrieves and returns the current user's recommendations.
        """
        try:
            current_user_id = get_jwt_identity()
            logging.info(f"Fetching recommendations for user ID: {current_user_id}")
            recommendations, status_code = recommender.fetch_recommendations()
            print("Recommendations\n:", recommendations)
            return recommendations, status_code
        except Exception as e:
            logging.error(f"Fetching recommendations error: {e}")
            return jsonify({"message": "Internal Server Error"}), 500
