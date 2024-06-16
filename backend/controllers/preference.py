from models.preference import Preference 
from models.engine.DBStorage import DbStorage 
from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

class Preferences:
    def __init__(self):
        self.storage = DbStorage()

    def create_preference(self):
        try:
            data = request.form()

            gender = data.get('gender', '').lower()
            min_age = int(data.get('min_age', 0))
            max_age = int(data.get('max_age', 0))
            country = data.get('country', '').lower()
            region = data.get('region', '').lower()
            industry_major = data.get('education_major', '').lower()  # e.g., health, IT, engineering
            fav_hobby = data.get('favourite_hobby', '')
            has_child = data.get('has_child', 'no').lower() == 'yes'
            wants_child = data.get('wants_child', 'yes').lower() == 'yes'
            
            user_id = get_jwt_identity()

            allowed_gender = ['male', 'female', 'transgender', 'non-binary']
            if gender not in allowed_gender:
                return jsonify({"message": "Loveefy does not recognize the gender"}), 400

            if min_age < 18:
                return jsonify({"message": "Teens below 18 are not allowed"}), 400
            
            if max_age > 200:
                return jsonify({"message": "Please pick a realistic max age"}), 400

            new_preference = Preference(
                gender=gender,
                min_age=min_age,
                max_age=max_age,
                country=country,
                region=region, 
                industry_major=industry_major,
                fav_hobby=fav_hobby,
                has_child=has_child,
                wants_child=wants_child,
                created_at=datetime.utcnow(),
                user_id=user_id
            )
            
            self.storage.new(new_preference)
            self.storage.save()
            return jsonify({"message": "User preference created successfully"}), 201
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500
