from datetime import datetime
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models.engine.DBStorage import DbStorage
from flask import jsonify, request
from models.user_profile import User_profile
from models.payment import Subscription

storage = DbStorage()

def restrict_unsubscribed_males(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        
        user = storage.get(User_profile, user_id=user_id)

        if user is None:
            return jsonify({"message": "User not found"}), 404

        if user.gender.lower() == "male":
            subscription = storage.get(Subscription, user_id=user_id)
            
            if not subscription or subscription.expiration_date is None:
                return jsonify({"message": "Please subscribe"}), 403
            
            if subscription.expiration_date < datetime.now():
                return jsonify({"message": "Your subscription has expired"}), 403

        return func(*args, **kwargs)
    
    return decorated_function
