#!/usr/bin/env python3
from models.engine.DBStorage import DbStorage
from models.matches import Matches
from flask import request
from flask_jwt_extended import get_jwt_identity

class Match:
    def ___init__(self):
        self.storage = DbStorage()

    def match(self):
        data = request.get_json()
        liked_users_ids = data.get('likedUsers', [])
        current_user_id = get_jwt_identity()
        
        for user_id in liked_users_ids:
            if user_id == current_user_id:
                continue
            existing_match = self._storage.get(Matches, user_id2=user_id, user_id1=current_user_id)
            if existing_match:
                return

            new_match = Matches(
                user_id1 = current_user_id,
                user_id2 = user_id
            )
