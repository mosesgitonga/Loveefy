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
           
            print('data:  ',data)
            gender = data.get('gender').lower()
            dob = data.get('dob')
            mobile_no = data.get('mobile_no')
            industry_major = data.get('industry_major', '').lower()
            education_level = data.get('education_level').lower()
            career = data.get('career').lower()
            has_child = data.get('has_child', 'no').lower()
            employment = data.get('employment').lower()
            is_schooling = data.get('is_schooling').lower()
            country = data.get('country').lower()
            region = data.get('region').lower()
            sub_region = data.get('sub_region').lower()

            print('details extracted!')
            # Validate age
            dob = datetime.strptime(dob, '%Y-%m-%d')
            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            print('age', age)
            if age <= 10:
                return make_response(jsonify({"message": "babies are not welcome. You should be breast feeding"}), 403)
            if age < 18:
                return make_response(jsonify({"message": "Kids are not welcome, go play video games"}), 403)
    

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
                mobile_no=mobile_no,
                user_id=user_id,
                industry_major=industry_major,
                education_level=education_level,
                career=career,
                employment=employment,
                is_schooling=is_schooling, 
                has_child=has_child,
                DOB=dob
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
            # self.storage.rollback()
            logger.error(f"Exception: {e}")
            return jsonify({"message": "Internal server error"}), 500

    def get_profile(self):
        try:
            user_id = get_jwt_identity()
            user_profile = self.storage.get(User_profile, user_id=user_id)
            profile_details = {
                "gender": user_profile.gender,
                "industry_major": user_profile.industry_major,
                "career": user_profile.career,
                "dob": user_profile.DOB
            }
            print(profile_details)
            return profile_details
        except Exception as e:
            logger.error(e)
            return jsonify({"message": "Internal Server Error"})

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

    def update_fields(self, data):
        try:
            id = get_jwt_identity()

            # Mapping fields to their corresponding models
            field_to_model = {
                'username': User,
                'gender': User_profile,
                'country': Place,
                'industry': User_profile,
                'career': User_profile,
                'dob': User_profile,
                'region': Place,
                'sub_region': Place,
                'age': User_profile,  # Assuming 'age' and 'mobile_no' belong to User_profile
                'mobile_no': User_profile,
                'subscription_type': User_profile  # Assuming this is part of User_profile
            }

            # Iterate over the fields in the request data
            for field, new_value in data.items():
                Get_object = field_to_model.get(field)
                if not Get_object:
                    logger.error(f"Attempted to update an unrecognized field: {field}")
                    continue  # Skip this field and continue with others

                # Fetch the correct object based on the field
                if Get_object == User_profile:
                    existing_user_profile = self.storage.get(Get_object, user_id=id)
                else:
                    existing_user_profile = self.storage.get(Get_object, id=id)

                if not existing_user_profile:
                    logger.error(f"User profile not found for user_id: {id}")
                    return jsonify({"message": "User profile not found"}), 404

                if hasattr(existing_user_profile, field):
                    setattr(existing_user_profile, field, new_value)
                    self.storage.new(existing_user_profile)
                    logger.info(f"Updated {field} to {new_value} for user profile {existing_user_profile.id}")
                else:
                    logger.error(f"Attempted to update non-existent field: {field}")
                    continue  # Skip this field and continue with others

            # Save the changes after all fields are updated
            self.storage.new(existing_user_profile)
            self.storage.save()
            return jsonify({"message": "Profile updated successfully"}), 200

        except Exception as e:
            logger.error(f"Exception while updating profile for user_id {id}: {e}")
            return jsonify({"message": "Internal server error"}), 500


if __name__ == '__main__':
    pass
