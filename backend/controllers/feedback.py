from models.report import Feedback
from models.engine.DBStorage import DbStorage
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

storage = DbStorage()
class FeedbackHandler:
    def __init__(self):
        self.storage = storage

    def create_feedback(self, data):
        user_id = get_jwt_identity()
        remarks = data.get('remarks')
        suggestions = data.get('suggestions')
        ratings = data.get('ratings')
        try:

            new_feedback = Feedback(
                user_id=user_id,
                remarks=remarks,
                suggestions=suggestions,
                ratings=ratings
            )
            self.storage.new(new_feedback)
            self.storage.save()
            return jsonify({"message": "We appreciate your feedback. Thank You"})
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal Server Error"})
