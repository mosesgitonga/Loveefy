#!/usr/bin/env python3
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from models.user import User 
from models.user_profile import User_profile
from dotenv import load_dotenv
import os

# Function to create all tables
def create_all_tables():
    # Create Flask application instance
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # Configure database
    user = os.getenv('MYSQL_USER')
    print(user)
    pwd = os.getenv('MYSQL_PASSWORD')
    host = os.getenv('HOST')
    db_name = os.getenv('MYSQL_DB')
    print(db_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{user}:{pwd}@{host}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    # Initialize SQLAlchemy
    db = SQLAlchemy(app)

    # Initialize models
    User()
    User_profile()

    with app.app_context():
        try:
            tables = db.create_all()
            if tables is None:
                print('tables were not created')
            else:
                print('table have been created')
        except Exception as e:
            print(f"Error {e}")