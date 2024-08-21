from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, leave_room, emit
from models.engine.DBStorage import DbStorage
from models.user import User
from models.messages import RoomMember
from routes.user_auth_route import auth_bp
from routes.user_profile_route import profile_bp
from routes.preference_route import preference_bp
from routes.upload_route import upload_bp
from routes.recommender_route import recommender_bp
from routes.matches.likes import likes_bp
from routes.messages import messages_bp
from routes.payments.Mpesa import mpesa_bp
from services.message import MessageService
from datetime import timedelta
from flask_cors import CORS
import os
from datetime import datetime

# Load environment variables
load_dotenv()
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

# Initialize services and storage
message = MessageService()
storage = DbStorage()
storage.reload()

# Initialize Flask app
app = Flask(__name__, static_folder='dist', static_url_path='')

# Initialize Socket.IO with logging
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")

# Set up CORS (limit to specific origins if needed)
CORS(app)

# Configure JWT
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)
jwt = JWTManager(app)

# Socket.IO event for user connection
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Socket.IO event for joining a room
@socketio.on('join_room')
@jwt_required()
def handle_join_room(data):
    try:
        print('Joining room ...')
        room_id = data['room_id']
        join_room(room_id)
    except Exception as e:
        emit('error', {'msg': 'Failed to join room'})
        print(f"Error joining room: {e}")

# Socket.IO event for leaving a room
@socketio.on('leave_room')
@jwt_required()
def handle_leave_room(data):
    try:
        room_id = data['room_id']
        leave_room(room_id)
    except Exception as e:
        emit('error', {'msg': 'Failed to leave room'})
        print(f"Error leaving room: {e}")

# Socket.IO event for sending a message
@socketio.on('send_message')
@jwt_required()
def handle_send_message(data):
    try:
        room_id = data['room_id']
        msg_content = data['content']
        user_id = get_jwt_identity()
        user = storage.get(User, id=user_id)
        username = user.username
        
        members = storage.get_all(RoomMember, room_id=room_id)
        receiver_id = next((member.user_id for member in members if member.user_id != user_id), None)

        if not receiver_id:
            emit('error', {'msg': 'No receiver found'})
            return
        
        # Save the message to the database
        message.save_message(
            sender_id=user_id,
            receiver_id=receiver_id,
            room_id=room_id,
            message=msg_content
        )

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        emit('receive_message', {'timestamp': timestamp, 'username': username, 'content': msg_content}, room=room_id)
    except Exception as e:
        emit('error', {'msg': 'Failed to send message'})
        print(f"Error sending message: {e}")


@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    print("Callback received:", data)
    return jsonify({"status": "success"})


# Serve the React application
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(preference_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(recommender_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(mpesa_bp)

# Main entry point
if __name__ == '__main__':
    # Run the app with eventlet for production readiness
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
