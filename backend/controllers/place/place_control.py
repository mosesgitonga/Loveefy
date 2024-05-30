#!/usr/bin/env python3
"""
handle the location of the user
"""
from flask_jwt_extended import  get_jwt_identity

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.place import Place
class Place_control:
    def __init__(self):
        self.storage = DbStorage()
        self.user_id = get_jwt_identity()

    def create_place(self, data):
        try:
            country = data.get('country')
            region = data.get('region')
            sub_region = data.get('sub_region')
            user_id = self.user_id


            new_place = Place(
                country = country,
                region=region,
                sub_region=sub_region,
                user_id=user_id
            )

            self.storage.new(new_place)
            self.storage.save()

            print('place created successfully')
            return jsonify({"message": "place created successfully"})
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server Error"})

    def update_place(self, data):
        try:
            user = self.storage.get(User, id=user_id)

            # update country
           
            if 'country' in data:
                user.users_profile.country = data['country']
                
            # update region
            region = kwargs['region']
            if region:
                user.users_profile.region = reg
            
            #update sub region
            sub_region = kwargs['sub_region']
            if sub_region:
                user.users_profile.sub_region = sub_region

        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server Error"})
