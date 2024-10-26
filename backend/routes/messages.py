from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.engine.DBStorage import DbStorage
from models.messages import RoomMember
import logging

from services.message import MessageService

messages = MessageService()
storage = DbStorage()
messages_bp = Blueprint('message', __name__, url_prefix="/api/v1/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@messages_bp.route('/rooms', methods=['GET'], strict_slashes=False)
@jwt_required()
def list_rooms():
    try:
        res = messages.list_rooms()
        return res  # Return the response directly if it's already JSON formatted
    except Exception as e:
        logger.error(f"Error listing rooms for user {get_jwt_identity()}: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
    
@messages_bp.route('/messages', methods=['GET'], strict_slashes=False)
@jwt_required()
def list_messages():
    try:
        res = messages.read_messages()
        return res 
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal Server Error"})
    
@messages_bp.route('/all_unread/count', methods=['GET'], strict_slashes=False)
@jwt_required()
def count_all_unread_messages():
    try:
        response = messages.count_all_unread_messages()
        return response
    except Exception as e:
        logger.info(e)
        return jsonify({"error": "Internal Server Error"})
    
@messages_bp.route('/unmatched_messages', methods=['POST'], strict_slashes=False)
@jwt_required()
def send_unmatched_users_messages():
    data = request.json 
    if 'user_id' not in data or 'msg_content' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    message_to_user_id = data['user_id']
    msg_content = data['msg_content']

    try:
        user_id = get_jwt_identity()

        room_id = messages.create_private_room(user_id, message_to_user_id)
        logger.info(f'room id: {room_id}')
        if not room_id:
            return jsonify({"error": "Failed to create room"}), 500

        members = storage.get_all(RoomMember, room_id=room_id)
        receiver_id = next((member.user_id for member in members if member.user_id != user_id), None)

        if not receiver_id:
            return jsonify({"error": "No valid receiver found"}), 400

        messages.save_message(
            sender_id=user_id,
            receiver_id=receiver_id,
            room_id=room_id,
            message=msg_content
        )
        return jsonify({"message": "Message sent successfully"}), 200

    except Exception as e:
        logger.error(f'Error: {e}')
        return jsonify({"message": "Internal Server Error"}), 500

    
