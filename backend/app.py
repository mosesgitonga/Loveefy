from flask_jwt_extended import JWTManager
from flask import Flask
from dotenv import load_dotenv
from models.engine.DBStorage import DbStorage
from routes.user_auth_route import auth_bp
from routes.user_profile_route import profile_bp
from routes.preference_route import preference_bp
from routes.upload_route import upload_bp
from datetime import timedelta
from flask_cors import CORS
import os

load_dotenv()
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

storage = DbStorage()
storage.reload()

app = Flask(__name__)
CORS(app)
CORS(auth_bp)
CORS(profile_bp)
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)

jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(preference_bp)
app.register_blueprint(upload_bp)

if __name__ == '__main__':
    app.run(debug=True)
