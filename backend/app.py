from flask_jwt_extended import JWTManager
from flask import Flask
from dotenv import load_dotenv
from models.engine.DBStorage import DbStorage
from views.user_auth_route import auth_bp
import os

load_dotenv()
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

storage = DbStorage()
storage.reload()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = jwt_secret_key

jwt = JWTManager(app)

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    debug=True
    app.run(debug=True)