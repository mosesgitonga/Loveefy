from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, make_response
from datetime import datetime
import os
import sys
import uuid
import MySQLdb
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.user_profile import User_profile
from models.place import Place
from models.user import User

class Profile:
    def __init__(self):
        self.storage = DbStorage()

    @jwt_required()
    def create_profile(self, data):
        try:
            user_id = get_jwt_identity()

            # Retrieve and validate data
            required_fields = ['gender', 'age', 'mobile_no', 'subscription_type']
            for field in required_fields:
                if not data.get(field):
                    return make_response(jsonify({"message": f"Missing required field: {field}"}), 400)

            gender = data.get('gender').lower()
            age = int(data.get('age'))
            mobile_no = data.get('mobile_no')
            subscription_type = data.get('subscription_type').lower()
            industry_major = data.get('industry_major', '').lower()
            fav_hobby = data.get('fav_hobby', '')
            has_child = data.get('has_child', 'no').lower()
            wants_child = data.get('wants_child', 'no').lower()
            country = data.get('country').lower()
            region = data.get('region').lower()
            sub_region = data.get('sub_region').lower()

            # Validate age
            if age < 18:
                return make_response(jsonify({"message": "Kids are not allowed, go play video games"}), 403)

            # Validate subscription and gender types
            if subscription_type not in ['free', 'gold', 'elite']:
                print('unknown subscription')
                return make_response(jsonify({"message": "Unknown subscription type"}), 400)
            if gender not in ['male', 'female']:
                return make_response(jsonify({"message": "Unknown gender"}), 400)

            # Check if profile already exists
            existing_profile = self.storage.check_existing_profile(user_id, mobile_no=mobile_no)
            existing_user = self.storage.get(User, id=user_id)
            if existing_profile:
                if existing_profile.user_id == user_id:
                    return make_response(jsonify({"message": "User already has a profile"}), 409)
                if existing_profile.mobile_no == mobile_no:
                    print('mobile number already exists')
                    return make_response(jsonify({"message": "Mobile number already exists"}), 409)

            # Create a new place if necessary
            new_place = Place(
                id=str(uuid.uuid4()),
                country=country,
                region=region,
                sub_region=sub_region,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            # Update user's place_id
            existing_user.place_id = new_place.id

            # Create a new user profile
            new_profile = User_profile(
                id=str(uuid.uuid4()),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                gender=gender,
                age=age,
                mobile_no=mobile_no,
                subscription_type=subscription_type,
                user_id=user_id,
                industry_major=industry_major,
                fav_hobby=fav_hobby,
                has_child=has_child,
            )

            # Use storage methods to handle session and transactions
            self.storage.new(new_place)
            self.storage.new(existing_user)
            self.storage.new(new_profile)
            self.storage.save()

            return jsonify({"message": "Profile created successfully"}), 201

        except MySQLdb._exceptions.IntegrityError as ie:
            self.storage.rollback()
            logger.error(f"IntegrityError: {ie}")
            return jsonify({"message": "Duplicate Entry"}), 409
        except Exception as e:
            #self.storage.rollback()
            logger.error(f"Exception: {e}")
            return jsonify({"message": "Internal server error"}), 500

    def delete_profile(self, profile_id):
        try:
            existing_user = self.storage.get(User_profile, id=profile_id)
            if existing_user:
                self.storage.delete(existing_user)
                self.storage.save()
                return jsonify({"message": f"User with id={existing_user.id} has been deleted"}), 200
            return jsonify({"message": "User does not exist"}), 404
        except Exception as e:
            logger.error(f"Exception: {e}")
            return jsonify({"message": "Internal server error"}), 500

    def update_field(self, id, field, new_value):
        try:
            existing_user_profile = self.storage.get(User_profile, id=id)
            if not existing_user_profile:
                return jsonify({"message": "User profile not found"}), 404

            setattr(existing_user_profile, field, new_value)
            self.storage.save()

            return jsonify({"message": f"{field} updated successfully"}), 200
        except Exception as e:
            logger.error(f"Exception: {e}")
            return jsonify({"message": "Internal server error"}), 500

    def update_username(self, data):
        return self.update_field(data['id'], 'username', data['new_update'])

    def update_gender(self, data):
        return self.update_field(data['id'], 'gender', data['new_update'])

    def update_age(self, data):
        return self.update_field(data['id'], 'age', data['new_update'])

    def update_mobile_no(self, data):
        return self.update_field(data['id'], 'mobile_no', data['new_update'])

    def update_subscription_type(self, data):
        return self.update_field(data['id'], 'subscription_type', data['new_update'])

if __name__ == '__main__':
    pass
