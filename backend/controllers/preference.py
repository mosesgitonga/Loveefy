from models.preference import Preference 
from models.user import User
from models.engine.DBStorage import DbStorage
from controllers.recommender.rule_based import Recommender
from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
import logging
import uuid

class Preferences:
    def __init__(self):
        self.storage = DbStorage()
        self.recommender = Recommender()
        self.logger = logging.getLogger(__name__)

    def create_preference(self):
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()  # Use get_json() for JSON payload

            # Extract data from the request payload
            gender = data.get('gender', '').lower()
            min_age = int(data.get('minAge', 0))
            max_age = int(data.get('maxAge', 0))
            country = data.get('country', '').lower()
            region = data.get('region', '').lower()
            industry_major = data.get('industryMajor', '').lower()
            career = data.get('career').lower()
            education_level = data.get('education_level').lower()
            employment = data.get('employment').lower()
            is_schooling = data.get('is_schooling').lower()
            fav_hobby = data.get('favHobby', '')
            has_child = data.get('hasChild', '').lower()
            wants_child = data.get('wantsChild', 'yes').lower()
            
            # Validate the input data
            allowed_gender = ['male', 'female', 'transgender', 'non-binary']
            if gender not in allowed_gender:
                return jsonify({"message": "Loveefy does not recognize the gender"}), 400

            if min_age < 18:
                return jsonify({"message": "Teens below 18 are not allowed"}), 400
            
            if max_age > 200:
                return jsonify({"message": "Please pick a realistic max age"}), 400

            current_user = self.storage.get(User, id=current_user_id)
            if not current_user:
                return jsonify({"message": "User not found"}), 404

            # Check if user already has a preference
            if current_user.preference_id:
                return jsonify({"message": "User already has a preference"}), 400

            # Create a new preference
            new_preference = Preference(
                id=str(uuid.uuid4()),
                gender=gender,
                min_age=min_age,
                max_age=max_age,
                country=country,
                region=region,
                industry_major=industry_major,
                career=career,
                education_level=education_level,
                employment=employment,
                is_schooling=is_schooling,
                fav_hobby=fav_hobby,
                wants_child=wants_child,
                created_at=datetime.now(),
            )
            
            # Associate the preference with the current user
            current_user.preference_id = new_preference.id

            # Save the new preference and update the user
            self.storage.new(new_preference)
            self.storage.new(current_user)
            self.storage.save()
            self.recommender.recommend_users()

            self.logger.info(f"Preference created successfully for user_id: {current_user_id}")

            return jsonify({"message": "User preference created successfully"}), 201
        except ValueError as ve:
            self.logger.error(f"Value error: {ve}")
            return jsonify({"message": "Invalid input"}), 400
        except Exception as e:
            self.logger.exception("Internal server error")
            return jsonify({"message": "Internal server error"}), 500
