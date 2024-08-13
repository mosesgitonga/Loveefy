from flask_jwt_extended import JWTManager
from flask import Flask
from dotenv import load_dotenv
from models.engine.DBStorage import DbStorage
from routes.user_auth_route import auth_bp
from routes.user_profile_route import profile_bp
from routes.preference_route import preference_bp
from routes.upload_route import upload_bp
from routes.recommender_route import recommender_bp
from routes.matches.likes import likes_bp
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

# Set up CORS
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Configure JWT
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(preference_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(recommender_bp)
app.register_blueprint(likes_bp)

if __name__ == '__main__':
    app.run(debug=True)
