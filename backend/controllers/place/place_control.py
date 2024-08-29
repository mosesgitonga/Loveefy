#!/usr/bin/env python3
"""
Module for handling user location functionalities in the application.

This module provides functionalities to create and update a user's location (place)
in the application. The location data is associated with a user and consists of
country, region, and sub-region.

Classes:
    Place_control: A controller class responsible for managing location data.

Functions:
    __init__(): Initializes the Place_control class with a DBStorage instance.
    create_place(data): Creates a new place for the current user if it doesn't already exist.
    update_place(data): Updates the existing place details for the current user.
"""

from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity
import os
import uuid
import sys
from datetime import datetime

current_file_path = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file_path, '..', '..', '..'))
sys.path.append(project_root)

from models.engine.DBStorage import DbStorage
from models.place import Place
from models.user import User

class Place_control:
    """
    Controller class for managing location data related to users.

    This class provides methods to create and update location data, which is 
    associated with a specific user in the database. The location data includes 
    country, region, and sub-region.

    Attributes:
        storage (DbStorage): An instance of the DbStorage class for database interaction.
    """

    def __init__(self):
        """Initializes the Place_control class with a DBStorage instance."""
        self.storage = DbStorage()

    def create_place(self, data):
        """
        Creates a new place for the current user if it doesn't already exist.

        Args:
            data (dict): A dictionary containing the following keys:
                - 'country': The country name.
                - 'region': The region name.
                - 'sub_region': The sub-region name.

        Returns:
            Response object: A JSON response indicating the result of the operation.
            - 409 Conflict if a place already exists for the user.
            - 201 OK if the place is successfully created.
            - 500 Internal Server Error if an error occurs.
        """
        try:
            country = data.get('country')
            region = data.get('region')
            sub_region = data.get('sub_region')
            user_id = get_jwt_identity()

            place = self.storage.get(Place, user_id=user_id)
            current_user = self.storage.get(User, id=user_id)
            if place is not None:
                return make_response(jsonify({"message": "place already exists"}), 409)

            new_place = Place(
                id=str(uuid.uuid4()),
                country=country,
                region=region,
                sub_region=sub_region,
                user_id=user_id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            self.storage.new(new_place)
            self.storage.save()
            current_user.place_id = new_place.user_id
            self.storage.new(current_user)
            self.storage.save()

            print('place created successfully')
            return jsonify({"message": "place created successfully"}), 201
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server Error"}), 500

    def update_place(self, data):
        """
        Updates the existing place details for the current user.

        Args:
            data (dict): A dictionary containing one or more of the following keys:
                - 'country': The updated country name.
                - 'region': The updated region name.
                - 'sub_region': The updated sub-region name.

        Returns:
            Response object: A JSON response indicating the result of the operation.
            - 500 Internal Server Error if an error occurs.
        """
        try:
            user_id = get_jwt_identity()
            user = self.storage.get(User, id=user_id)

            # Update country
            if 'country' in data:
                user.users_profile.country = data['country']

            # Update region
            region = data.get('region')
            if region:
                user.users_profile.region = region

            # Update sub-region
            sub_region = data.get('sub_region')
            if sub_region:
                user.users_profile.sub_region = sub_region

            self.storage.save()

            return jsonify({"message": "place updated successfully"})
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server Error"}), 500
