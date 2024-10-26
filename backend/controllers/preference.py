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
            data = request.get_json()  
            print(data)

            # Extract data from the request payload
            gender = data.get('gender', '').lower()
            min_age = int(data.get('minAge'))
            max_age = int(data.get('maxAge'))
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
            allowed_gender = ['male', 'female']
            if gender not in allowed_gender:
                return {"message": "Loveefy does not recognize this gender"}, 400

            if min_age < 18:
                return {"message": "kids below 18 are not allowed"}, 400
            
            if max_age > 200:
                return {"message": "Please pick a realistic max age"}, 400

            current_user = self.storage.get(User, id=current_user_id)
            if not current_user:
                return {"message": "User not found"}, 404

            # Check if user already has a preference
            if current_user.preference_id:
                return {"message": "User already has a preference"}, 400

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

            return {"message": "User preference created successfully"}, 201
        except ValueError as ve:
            self.logger.error(f"Value error: {ve}")
            return {"message": "Invalid input"}, 400
        except Exception as e:
            self.logger.exception("Internal server error")
            return {"message": "Internal server error"}, 500
        
    def show_preference(self):
        user_id = get_jwt_identity()
        print(user_id)
        try:
            user = self.storage.get(User, id=user_id)
            if not user:
                return jsonify({"error": "did not find user"}), 404
            preferences = self.storage.get(Preference, id=user.preference_id)
            preferences = {
                "gender": preferences.gender,
                "industry_major": preferences.industry_major,
                "career": preferences.career,
                "country": preferences.country,
                "region": preferences.region,
                "min_age": preferences.min_age,
                "max_age": preferences.max_age,

            }
            print(preferences)
            if not preferences:
                return jsonify({"error": "did not find any preference"}), 404
            return jsonify({"message": preferences}), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal Server Error"}), 500

    def patch_preferences(self, data):
        # updates specific preferences
        if not data:
            return jsonify({"message": "No data to update"}), 400  # 400 for Bad Request

        gender = data.get('gender')
        industry_major = data.get('industry_major')
        career = data.get('career')
        min_age = data.get('minAge')
        max_age = data.get('max_age')
        education_level = data.get('education_level')
        education_status = data.get('education_status')

        try:
            user_id = get_jwt_identity()
            user = self.storage.get(User, id=user_id)
            print('preference id',user.preference_id)
            preference = self.storage.get(Preference, id=user.preference_id)
            print('preference  d',preference)

            if not preference:
                print('preference not found\n')
                return jsonify({"message": "Preferences not found"}), 404 

            # Update preferences if provided
            if gender:
                preference.gender = gender
                self.storage.new(preference)
            if industry_major:
                preference.industry_major = industry_major
                self.storage.new(preference)
            if career:
                preference.career = career
                self.storage.new(preference)
            if min_age:
                preference.min_age = min_age
                self.storage.new(preference)
            if max_age:
                preference.max_age = max_age
                self.storage.new(preference)
            if education_level:
                preference.education_level = education_level
                self.storage.new(preference)
            if education_status:
                preference.education_status = education_status
                self.storage.new(preference)
            self.storage.save()

            return jsonify({"message": "Preferences updated successfully"}), 200

        except Exception as e:
            print(f"Error updating preferences: {e}")
            return jsonify({"message": "Internal Server Error"}), 500 
