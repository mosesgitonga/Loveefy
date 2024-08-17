from models.messages import Messages, Room, RoomMember
from models.engine.DBStorage import DbStorage
from models.user import User
from models.messages import Messages
from flask import jsonify, request 
from flask_jwt_extended import get_jwt_identity
import uuid

class MessageService:
    def __init__(self):
        self.storage = DbStorage()

    def create_private_room(self, user_id1, user_id2):
        try:
            sorted_ids = sorted([user_id1, user_id2])
            room_id = f"{sorted_ids[0][-16:]}_{sorted_ids[1][-16:]}"  # Use last 16 characters of user IDs for the room ID
            
            existing_room = self.storage.get(Room, id=room_id)
            if existing_room:
                return jsonify({"message": "Room already exists", "room_id": existing_room.id}), 200
            
            new_room = Room(id=room_id) 
            self.storage.new(new_room)
            self.storage.save()

            # Add members to the room
            new_member1 = RoomMember(id=str(uuid.uuid4()), user_id=user_id1, room_id=room_id)
            new_member2 = RoomMember(id=str(uuid.uuid4()), user_id=user_id2, room_id=room_id)
            self.storage.new(new_member1)
            self.storage.new(new_member2)
            self.storage.save()

            return jsonify({"message": "Private room created", "room_id": new_room.id}), 201
        except Exception as e:
            print(f"Error creating room: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
        
    def list_rooms(self):
        try:
            current_user_id = get_jwt_identity()

            # Fetch all room memberships for the current user
            room_memberships = self.storage.get_all(RoomMember, user_id=current_user_id)
            room_ids = [membership.room_id for membership in room_memberships]

            # Fetch rooms based on the IDs
            rooms = self.storage.get_multiple(Room, ids=room_ids)
            
            rooms_data = []
            for room in rooms:
                # Fetch all members in this room
                members = self.storage.get_all(RoomMember, room_id=room.id)
                member_ids = [member.user_id for member in members]

                # Identify the opposite user in the room
                opposite_user_id = next((user_id for user_id in member_ids if user_id != current_user_id), None)
                
                if opposite_user_id:
                    opposite_user = self.storage.get(User, id=opposite_user_id)

                    room_data = {
                        "room_id": room.id,
                        "name": room.name,
                        "created_at": room.created_at,
                        "opposite_username": opposite_user.username,
                        "opposite_id": opposite_user.id
                    }
                    rooms_data.append(room_data)

            return jsonify(rooms_data), 200
        except Exception as e:
            print(f"Error listing rooms: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
        
    def save_message(self, message, room_id, sender_id, receiver_id):
        try:
            print('saving message...')

            new_message = Messages(
                                id=uuid.uuid4(),
                                room_id=room_id,
                                sender_Id=sender_id,
                                receiver_id=receiver_id,
                                content=message,
                                    )
            self.storage.new(new_message)
            self.storage.save()
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal Server Error"})
        
    def read_messages(self):
        try:
            room_id = request.args.get('roomId')
            page = request.args.get('page', default=1, type=int)  # Default to page 1 if not provided
            per_page = request.args.get('per_page', default=30, type=int)  # Default to 30 per page if not provided
            
            messages = self.storage.get_all(Messages, page=page, per_page=per_page, room_id=room_id)

            messages = sorted(messages, key=lambda message: message.time)
            message_data = [
                {
                    "id": message.id,
                    "room_id": message.room_id,
                    "content": message.content,
                    "time": message.time,
                    "sender_id": message.sender_Id,
                    "receiver_id": message.receiver_id,
                    "username": self.storage.get(User, id=message.sender_Id).username
                }
                for message in messages
            ]

            if not messages:
                username = [self.storage.get(User, id=message.sender_Id).username for message in messages]
                message_data = [{"username": "System", "content": "Congratulations! You've matched! Say hello or tell a joke—just don’t start with ‘Knock knock’!"}]
            
            return jsonify({"messages": message_data})
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal Server Error"}), 500
    
