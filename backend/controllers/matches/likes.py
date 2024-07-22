from models.engine.DBStorage import DbStorage
from models.matches import Likes
from models.user import User  # Ensure this import if not already imported
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
import logging
import uuid
from sqlalchemy.exc import IntegrityError

class LikesService:
    def __init__(self):
        self.storage = DbStorage()
        self.user_id = get_jwt_identity()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def create_likes(self):
        """
        Creates likes to be used for matches
        """
        try:
            data = request.get_json()
            if not data or 'likedUsers' not in data:
                return jsonify({"message": "Invalid input"}), 400

            liked_user_ids = data.get('likedUsers', [])
            if not liked_user_ids:
                return jsonify({"message": "No users to like provided"}), 400

            with self.storage.get_session() as session:
                valid_likes = []
                for liked_user_id in liked_user_ids:
                    liked_user = session.query(User).filter_by(id=liked_user_id).first()
                    if not liked_user:
                        self.logger.error(f"User with id {liked_user_id} does not exist.")
                        continue

                    existing_like = session.query(Likes).filter_by(user_id=self.user_id, liked_id=liked_user_id).first()
                    if existing_like:
                        self.logger.info(f'Like already exists for user {liked_user_id}')
                        continue

                    existing_like = session.query(Likes).filter_by(user_id=liked_user_id, liked_id=self.user_id).first()
                    if existing_like:
                        self.logger.info(f'Like already exists for user {liked_user_id}')
                        continue

                    new_like = Likes(
                        id=str(uuid.uuid4()),
                        user_id=self.user_id,
                        liked_id=liked_user_id
                    )
                    print(new_like)
                    valid_likes.append(new_like)

                if valid_likes:
                    session.bulk_save_objects(valid_likes)
                    session.commit()
                    self.logger.info('Likes created successfully')
                    return jsonify({"message": "Likes created successfully"}), 201
                else:
                    return jsonify({"message": "No valid likes to create"}), 400

        except IntegrityError as e:
            self.storage.rollback()
            self.logger.error(f"Integrity error: {e.orig.args}")
            return jsonify({"message": "Integrity error"}), 400
        except Exception as e:
            self.logger.error(f"Internal server error: {e}")
            return jsonify({"message": "Internal server error"}), 500
