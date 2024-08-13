from models.engine.DBStorage import DbStorage
from models.matches import Likes, Matches
from models.user import User 
from models.notification import Notification
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
import logging
import uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class LikesService:
    def __init__(self):
        self.storage = DbStorage()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @jwt_required()
    def create_likes(self):
        """
        Handles the logic for liking a user and potentially creating a match.
        """
        try:
            liker_id = get_jwt_identity()  # Assuming the liker is the current user
            liked_id = request.json.get('liked_id')

            if not liked_id:
                return jsonify({"message": "Liked user ID is required"}), 400

            # Check if the like already exists
            existing_like = self.storage.get(Likes, liked_id=liked_id, user_id=liker_id)
            if existing_like:
                return jsonify({"message": "Like already exists"}), 200

            # Create a new Like record
            new_like = Likes(
                user_id=liker_id,
                liked_id=liked_id
            )
            self.storage.new(new_like)
            self.storage.save()

            # Check if the liked user has also liked the liker (to create a match)
            reciprocal_like = self.storage.get(Likes, user_id=liked_id, liked_id=liker_id)

            if reciprocal_like:
                # Create a match if both users liked each other
                new_match = Matches(
                    id=str(uuid.uuid4()),
                    user_id1=liker_id,
                    user_id2=liked_id,
                    status='pending'
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
            else:
                # If no match, just notify the liked user of the new like
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

                return jsonify({"message": "User liked successfully, waiting for their response."}), 200

        except IntegrityError as e:
            self.storage.rollback()
            self.logger.error(f"Integrity error: {e.orig.args}")
            return jsonify({"message": "Integrity error"}), 400
        except Exception as e:
            self.storage.rollback()
            self.logger.error(f"Internal server error: {e}")
            return jsonify({"message": "Internal server error"}), 500
