from models.engine.DBStorage import DbStorage
from models.matches import Likes, Matches
from models.user import User 
from models.user_profile import User_profile
from models.uploads import Upload
from models.notification import Notification
from services.message import MessageService
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
import logging
import uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from contextlib import contextmanager
from datetime import datetime

def calculate_age(dob):
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

class LikesService:
    def __init__(self):
        self.storage = DbStorage()
        self.messageService = MessageService()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def transaction(self):
        try:
            yield
            self.storage.save()
        except Exception as e:
            self.storage.rollback()
            self.logger.error(f"Transaction failed: {e}")
            raise

    @jwt_required()
    def create_likes(self):
        liker_id = get_jwt_identity()
        liked_id = request.json.get('liked_id')

        if not liked_id:
            return jsonify({"message": "Liked user ID is required"}), 400

        try:
            existing_like = self.storage.get(Likes, liked_id=liked_id, user_id=liker_id)
            if existing_like:
                return jsonify({"message": "Like already exists"}), 200

            with self.transaction():
                new_like = Likes(user_id=liker_id, liked_id=liked_id)
                self.storage.new(new_like)

                if self._is_reciprocal_like(liker_id, liked_id):
                    return self._create_match(liker_id, liked_id)

                self._notify_new_like(liker_id, liked_id)

                return jsonify({"message": "User liked successfully, waiting for their response."}), 200

        except IntegrityError as e:
            self.logger.error(f"Integrity error: {e.orig.args}")
            return jsonify({"message": "Integrity error"}), 400
        except SQLAlchemyError as e:
            self.logger.error(f"Database error: {e}")
            return jsonify({"message": "Database error"}), 500
        except Exception as e:
            self.logger.error(f"Internal server error: {e}")
            return jsonify({"message": "Internal server error"}), 500

    def _is_reciprocal_like(self, liker_id, liked_id):
        reciprocal_like = self.storage.get(Likes, user_id=liked_id, liked_id=liker_id)
        return reciprocal_like is not None

    def _create_match(self, liker_id, liked_id):
        existing_match = self.storage.get(Matches, user_id1=liker_id, user_id2=liked_id)
        if existing_match:
            self.logger.info("Match already exists")
            return jsonify({"message": "Match already exists"}), 200

        room = self.messageService.create_private_room(liker_id, liked_id)

        new_match = Matches(
            id=str(uuid.uuid4()),
            user_id1=liker_id,
            user_id2=liked_id,
            status='matched'
        )
        self.storage.new(new_match)
        self.storage.save()

        # Create a notification for the liked user
        notification_message = "It's a match! You both liked each other."
        notification = Notification(
            id=str(uuid.uuid4()),
            user_to_id=liked_id,
            user_from_id=liker_id,
            message=notification_message
        )
        self.storage.new(notification)
        self.storage.save()

        return jsonify({"message": notification_message}), 200

    def _notify_new_like(self, liker_id, liked_id):
        existing_notification = self.storage.get(Notification, user_to_id=liked_id, user_from_id=liker_id)

        if not existing_notification:
            notification = Notification(
                id=str(uuid.uuid4()),
                user_to_id=liked_id,
                user_from_id=liker_id,
                message="You have a new like!" 
            )
            self.storage.new(notification)
            self.storage.save()

    def likeback(self):
        try:
            print('liking back...')
            data = request.get_json()  # Correct method to get JSON data
            print(data)
            liked_id = data.get('userId')
            liker_id = get_jwt_identity()
            notification_id = data.get('notificationId')
            print({"type": type(liked_id), "liked id":liked_id})
            print(type(notification_id))
            print('notification id: ', notification_id)
            if liked_id is None or notification_id is None:
                print('missing')
                return jsonify({"message": "user_id and notificationId are required."}), 400
            print('data present!\n')
            # Ensure that `_create_match` returns a response
            match_response = self._create_match(liker_id, liked_id)
            if match_response:
                notification = self.storage.get(Notification, id=notification_id)
                self.storage.delete(obj=notification)
                self.storage.save()
                return match_response



            return jsonify({"message": "Match created and notification removed."}), 201

        except Exception as e:
            self.logger.error(f"Error in likeback: {e}")
            return jsonify({"message": "Internal Server Error"}), 500



    def list_notifications(self):
        try:
            current_user_id = get_jwt_identity()
            if not current_user_id:
                return jsonify({"message": "User not identified. Please login."}), 401

            notifications = self.storage.get_all(Notification, user_to_id=current_user_id)
            if not notifications:
                return jsonify({"message": "No notifications found."}), 200

            # Get all unique user_from_ids
            user_ids = {notification.user_from_id for notification in notifications}
            
            # Fetch all user details in one go
            users = self.storage.get_multiple(User, ids=list(user_ids))
            user_images = self.storage.get_multiple(Upload, [user.id for user in users])
            user_profiles = self.storage.get_multiple(User_profile, [user.id for user in users])

            # Map user details for quick access
            user_dict = {user.id: user.username for user in users}
            user_image_dict = {image.user_id: image.image_path for image in user_images}
            user_profile_dict = {profile.user_id: profile for profile in user_profiles}

            # Create the list of notifications
            notifications_list = [
                {
                    "id": notification.id,
                    "message": notification.message,
                    "from_username": user_dict.get(notification.user_from_id),
                    "from_user_id": notification.user_from_id,
                    "timestamp": notification.created_at,
                    "image_path": user_image_dict.get(notification.user_from_id),
                    "industry": user_profile_dict[notification.user_from_id].industry_major,
                    "career": user_profile_dict[notification.user_from_id].career,
                    "age": calculate_age(user_profile_dict[notification.user_from_id].DOB),  # Calculate age here
                    "gender": user_profile_dict[notification.user_from_id].gender,
                    "employment": user_profile_dict[notification.user_from_id].employment,
                    "education_level": user_profile_dict[notification.user_from_id].education_level
                }
                for notification in notifications
            ]

            return jsonify({"notifications": notifications_list}), 200

        except Exception as e:
            self.logger.error(f"Error listing notifications: {e}")
            return jsonify({"message": "Internal Server Error"}), 500

    def reject(self, data):
        try:
            rejected_id = data.get('rejected_id')
            user_id = get_jwt_identity()

            notification = self.storage.get(Notification, user_to_id=user_id, user_from_id=rejected_id, message="You have a new like!")
            like = self.storage.get(Likes, liked_id=user_id, user_id=rejected_id)

            self.storage.delete(notification)
            self.storage.delete(like)

            self.storage.save()
            return jsonify({"message": "notification deleted"}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal Server Error"})
    
