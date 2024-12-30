#!/usr/bin/env python3
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Api, Resource, fields, Namespace
import logging
from controllers.recommender.rule_based import Recommender

logging.basicConfig(level=logging.INFO)

# Initialize Recommender and Blueprint
recommender = Recommender()
recommender_api = Namespace('v1/', description="Recommendation API endpoints")


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
    @recommender_api.param('page', 'The page number for pagination', type=int, default=1, required=False)
    @recommender_api.param('per_page', 'Number of recommendations per page', type=int, default=12, required=False)
    @recommender_api.response(200, 'Recommendations successfully retrieved')
    @recommender_api.response(500, 'Internal Server Error')
    def get(self):
        """
        GET /recommendations
        ---
        Retrieves and returns the current user's recommendations.
        """
        try:
            page = request.args.get('page', default=1, type=int)
            per_page=request.args.get('per_page', default=12, type=int)
            current_user_id = get_jwt_identity()
            logging.info(f"Fetching recommendations for user ID: {current_user_id}")
            recommendations, status_code = recommender.fetch_recommendations(page=page, per_page=per_page)
            return recommendations, status_code
        except Exception as e:
            logging.error(f"Fetching recommendations error: {e}")
            return jsonify({"message": "Internal Server Error"}), 500
