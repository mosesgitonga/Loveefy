from flask import Flask
from models.engine.DBStorage import DbStorage

app = Flask(__name__)
db_storage = DbStorage(app)