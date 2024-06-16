#!/usr/bin/env python3
"""
handle the location of the user
"""
from flask import jsonify, make_response
from flask_jwt_extended import  get_jwt_identity
import os
import uuid
import sys
from datetime import datetime
current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.place import Place

class Place_control:
    def __init__(self):
        self.storage = DbStorage()
        #self.

    def create_place(self, data):
        try:
            country = data.get('country')
            region = data.get('region')
            sub_region = data.get('sub_region')
            user_id = get_jwt_identity()
            
            place = self.storage.get(Place, user_id=user_id)
            if place is not None:
                return make_response(jsonify({"message": "place already exists"}), 409)
            new_place = Place(
                id=str(uuid.uuid4()),
                country = country,
                region=region,
                sub_region=sub_region,
                user_id=user_id,
                created_at=datetime.now(),
                updated_at=datetime.now()
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
            user_id = get_jwt_identity()
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
