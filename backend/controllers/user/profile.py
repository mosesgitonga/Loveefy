from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify
from datetime import datetime
import os
import sys
import uuid
import MySQLdb

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.user_profile import User_profile

class Profile():
    def __init__(self):
        self.storage = DbStorage()

    def create_profile(self, data):
        try:
            username = data.get('username')
            gender = data.get('gender')
            age = data.get('age')
            mobile_no = data.get('mobile_no')
            subscription_type = data.get('subscription_type')
            user_id = get_jwt_identity()
            print(user_id)

            # check if user already exists
            existing_profile = self.storage.check_existing_profile(user_id, username, mobile_no)
            if existing_profile:
                if existing_profile.user_id == user_id:
                    print('User already has a profile')
                    return jsonify({"message": "User already has a profile"})
                if existing_profile.username == username:
                    print({"message": "username already exists"})
                    return jsonify({"message": "Username already exists"})
                if existing_profile.mobile_no == mobile_no:
                    print('mobile no already exists')
                    return jsonify({"message": "mobile no already exists"})

            if not all([gender, age, mobile_no, subscription_type, user_id]):
                print('key words were not retrieved')
                return jsonify({"message": "missing required fields"})

            if age < 18:
                print('under age user is not allowed')
                return jsonify({"message": "Kids are not alowed"})

            subscription_types = ['free', 'gold']
            gender_types = ['male', 'female']
            if subscription_type not in subscription_types:
                return jsonify({"message": "unknown subscription type"}), 400
            if gender not in gender_types:
                return jsonify({"message": "unknown gender"}), 400
                
        
            new_profile = User_profile(
                id=str(uuid.uuid4()),
                created_at=datetime.now(),
                username=username,
                gender=gender,
                age=age,
                mobile_no=mobile_no,
                subscription_type=subscription_type,
                user_id=user_id
            )

            self.storage.new(new_profile)
            self.storage.save()
            print('profile has been created')

            return jsonify({"message": "profile created successfully"}), 200
        except MySQLdb._exceptions.IntegrityError as ie:
            print(ie)
            return jsonify({"message": "Duplicate Entry"})
        except Exception as e:
            print(e)
            return "Internal server error", 500

    def delete_profile(self, profile_id):
        try:
            existing_user = self.storage.get(User_profile, id=profile_id)
            if existing_user:
                deleted_obj = self.storage.delete(existing_user)
                self.storage.save()
                return jsonify({f"message": "user of id={existing_user.id} has been deleted"})
            return jsonify({"message": "user does not exist"})
        except Exception as e:
            print(e)
            return jsonify({"messsage": "Internal servetr errror"})

    def update_username(self, data):
        try:
            new_username = data['new_update']
            username=data['username']

            #check if the new_username already exists
            new_username_existence = self.storage.get(User_profile, username=new_username)
            if new_username_existence is not None:
                print('The new username Already exists')
                return jsonify({"message": "username already exists"}), 400

            existing_user_profile = self.storage.get(User_profile, username=username)
            if not existing_user_profile:
                return jsonify({"message": "user profile not found"}), 404

            # update username
            if username:
                existing_user_profile.username = new_username
                self.storage.new(existing_user_profile)
                self.storage.save()
                print('after update', existing_user_profile.username)
                if existing_user_profile.username == new_username:
                    print('update was successful')
                    return jsonify({"message": "username updated succesfully"}), 200
                print('update UNsuccessful')

        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    def update_gender(self, data):
        try:
            # update gender
            gender = data['gender']
            new_gender = data['new_update']
            if gender:
                existing_user_profile.gender = new_gender
                self.storage.new(existing_user_profile)
                self.save()
                if existing_user_profile.gender == new_gender:
                    print('gender has been updated')
                    return jsonify({"message": "gender has been updated"}), 200
                return jsonify({"message": "gender has not be updated"}), 400

        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"})

    def update_age(self, data):
        try:
            #update age
            age = data['age']
            new_age = data['new_update']
            if age:
                existing_user_profile.age = new_age
                self.storage.new(existing_user_profile)
                self.save()
                if existing_profile.age == new_age:
                    return jsonify({"message","update was successful"}), 200
                return jsonify({"message": "update not successful"}), 400
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"})

    def update_mobile_no(self, data):
        try:
            # update mobile no
            mobile_no = data['mobile_no']
            new_mobile_no = data['new_update']
            if mobile_no:
                existing_user_profile.mobile_no = new_mobile_no
                self.storage.new(existing_user_profile)
                self.storage.save()
                if existing_user_profile.mobile_no == new_mobile_no:
                    print('update successful')
                    return jsonify({"message": "update was successful"}), 200
                return jsonify({"message": "update was unsuccessful"}), 400
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"})
    
    def update_subscription_type(self, data):
        try:
            # update subscription type
            subscription_type = data['subscription_type']
            new_subscription_type = data['new_update']
            if susbscription_type:
                existing_user_profile.subscription_type = new_subscription_type
                if existing_user_profile.subscription_type == new_subscription_type:
                    print('update successul')
                    return jsonify({"message": "update successful"}), 200
                print('unsuccesful updated')
                return jsonify({"message": "Unsuccessful update"}), 400
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"})
        
if __name__ == '__main__':
    pass