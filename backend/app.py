from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, decode_token
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_mail import Mail, Message
from flask_redis import FlaskRedis
from models.engine.DBStorage import DbStorage
from models.user import User
from models.messages import RoomMember, Messages
from routes.user_auth_route import auth_bp
from routes.user_profile_route import profile_bp
from routes.preference_route import preference_bp
from routes.upload_route import upload_bp
from routes.recommender_route import recommender_bp
from routes.matches.likes import likes_bp
from routes.messages import messages_bp
from routes.payments.Mpesa import mpesa_bp
from routes.notifications import notifications_bp
from routes.feedback_route import feedback_bp
from services.message import MessageService
from controllers.user.user_auth import User_auth
from datetime import timedelta
from flask_cors import CORS
import redis
import os
import secrets
from datetime import datetime

# Load environment variables
load_dotenv()
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

# Initialize services and storage
message = MessageService()
storage = DbStorage()
storage.reload()

# Initialize Flask app
app = Flask(__name__, static_folder='./dist', static_url_path='')

CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")


@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

# Configuration settings
app.config['REDIS_URL'] = "redis://localhost:6379/0"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'infosec947@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'infosec947@gmail.com'
SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(10)
SECURITY_PASSWORD_SALT = secrets.token_hex(11)


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
mail = Mail(app)



user_auth = User_auth(mail=mail)

# Configure JWT
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)
jwt = JWTManager(app)

# Socket.IO event for user connection
@socketio.on('connect')
def handle_connect():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(' ')[1]  # Extract token part from "Bearer <token>"
        try:
            decoded_token = decode_token(token)
            print("User authenticated:", decoded_token)
        except Exception as e:
            print("JWT verification failed:", e)
            return
    else:
        print("Missing Authorization Header")
        return

# Utility Functions for Room Handling
def join_room_util(room_id):
    try:
        print(f'Joining room {room_id}...')
    
        join_room(room_id)
    except Exception as e:
        print(f"Error joining room: {e}")
        emit('error', {'msg': f'Failed to join room: {str(e)}'})

def leave_room_util(room_id):
    try:
        print(f'Leaving room {room_id}...')
        leave_room(room_id)
    except Exception as e:
        print(f"Error leaving room: {e}")
        emit('error', {'msg': f'Failed to leave room: {str(e)}'})

# Socket.IO event for joining a room
@socketio.on('join_room')
def handle_join_room(data):
    room_id = data.get('room_id')
    if not room_id:
        print('no room id received')
        return
    try:
        unread_messages = storage.get_all(Messages, room_id=room_id, status="unread")
        print('unread messages', unread_messages)
        for message in unread_messages:
            message.status = "read"
            storage.new(message)
        storage.save()
        join_room_util(room_id)
    except Exception as e:
        print('was not able to join room\n')
        return jsonify({"message": "Internal Server Error"})

# Socket.IO event for leaving a room
@socketio.on('leave_room')
def handle_leave_room(data):
    room_id = data.get('room_id')
    leave_room_util(room_id)

# Socket.IO event for sending a message
@socketio.on('send_message')
def handle_send_message(data):
    try:
        token = data.get('token')
        if token is None:
            emit('error', {'msg': 'Missing token'})
            return

        # Decode and verify the token
        try:
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
        except Exception as e:
            print("JWT verification failed:", e)
            emit('error', {'msg': 'Invalid token'})
            return

        # Proceed with handling the message after JWT verification
        room_id = data['room_id']
        msg_content = data['content']
        user = storage.get(User, id=user_id)
        username = user.username

        # Validate the room and get receiver ID
        members = storage.get_all(RoomMember, room_id=room_id)
        receiver_id = next((member.user_id for member in members if member.user_id != user_id), None)

        if not receiver_id:
            emit('error', {'msg': 'No receiver found'})
            return

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save the message to the database
        message.save_message(
            sender_id=user_id,
            receiver_id=receiver_id,
            room_id=room_id,
            message=msg_content
        )

        # Emit the message to the room
        print(f'emitting message to {room_id} content {msg_content} from {username}\n\n\n')

        emit('receive_message', {'timestamp': timestamp, 'username': username, 'content': msg_content}, room=room_id)

    except Exception as e:
        emit('error', {'msg': 'Failed to send message'})
        print(f"Error sending message: {e}")



@app.route('/', methods=['GET'])
def main():
    return send_from_directory('./dist', 'index.html')

@app.route('/static/<path:filename>', methods=['GET'])
def serve_static_files(filename):
    return send_from_directory('./dist/static', filename)


 
@app.route('/uploads/<path:filename>', methods=['GET'])
def get_uploaded_file(filename):
    try:
        return send_from_directory('./uploads', filename)
    except FileNotFoundError:
        return jsonify({"message": "File not found"}), 404



# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(preference_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(recommender_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(mpesa_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(feedback_bp)



# Main entry point
if __name__ == '__main__':
    # Run the app with eventlet for production readiness
    socketio.run(app, host='0.0.0.0', port=5000)
