from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.user_profile import User_profile

class Profile():
    def __init__(self):
        self.storage = DbStorage()

    def create_profile(self, data):
        username = data.get('username')
        gender = data.get('gender')
        age = data.get('age')
        mobile_no = data.get('mobile_no')
        subscription_type = data.get('subscription_type')
        user_id = get_jwt_identity()

        if not all([gender, age, mobile_no, subscription_type, preference, user_id]):
            print('key words were not retrieved')
            return

        if age < 18:
            print('under age user is not allowed')
            return jsonify(message='Sorry, kids are not allowed')

        subscription_types, gender_types = ['free, gold'], ['male', 'female']
        if subscription_type not in subscription_types:
            return jsonify(message="Unknown subscription type")
        if gender not in gender_types:
            return jsonify(message='Unknown gender')
            
    
        new_profile = User_profile(
            gender=gender,
            age=age,
            mobile_no=mobile_no,
            subscription_type=subscription_type,
            user_id=user_id
        )

        self.storage.new(new_profile)
        self.storage.save()
        print('profile has been created')

        return new_profile

if __name__ == '__main__':
    pass