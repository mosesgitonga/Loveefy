from flask import Flask
from dotenv import load_dotenv
import os


class DbStorage:
    def __init__(self):
        

if __name__ == '__main__':
    storage = DbStorage()
    app = Flask(__name__)
    if app:
        print('app created successfully')
        storage.init_app(app)
    else:
        print('some err')