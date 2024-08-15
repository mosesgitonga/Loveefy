from flask_jwt_extended import JWTManager, jwt_required, decode_token
from flask import Flask, request
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, send, leave_room, emit, disconnect
from models.engine.DBStorage import DbStorage
from routes.user_auth_route import auth_bp
from routes.user_profile_route import profile_bp
from routes.preference_route import preference_bp
from routes.upload_route import upload_bp
from routes.recommender_route import recommender_bp
from routes.matches.likes import likes_bp
from routes.messages import messages_bp
from datetime import timedelta
from flask_cors import CORS
import os

# Load environment variables
load_dotenv()
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

# Initialize database storage
storage = DbStorage()
storage.reload()

# Initialize Flask app
app = Flask(__name__)

# Initialize Socket.IO with logging
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")


# Set up CORS (limit to specific origins if needed)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure JWT
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)
jwt = JWTManager(app)

# Socket.IO event for user connection
@socketio.on('connect')
def handle_connect():
    print('client connected')
  
# Socket.IO event for joining a room
@socketio.on('join_room')
@jwt_required()
def handle_join_room(data):
    try:
        room_id = data['room_id']
        join_room(room_id)
        send(f"User {data['username']} has joined the room", room=room_id)
    except Exception as e:
        emit('error', {'msg': 'Failed to join room'})
        print(f"Error joining room: {e}")

# Socket.IO event for leaving a room
@socketio.on('leave_room')
@jwt_required()
def handle_leave_room(data):
    try:
        username = data['username']
        room_id = data['room_id']
        leave_room(room_id)
        emit('message', {'msg': f'{username} has left the room'}, room=room_id)
    except Exception as e:
        emit('error', {'msg': 'Failed to leave room'})
        print(f"Error leaving room: {e}")


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(preference_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(recommender_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(messages_bp)

# Main entry point
if __name__ == '__main__':
    # Run the app with eventlet for production readiness
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)