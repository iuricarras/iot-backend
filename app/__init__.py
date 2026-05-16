import os
from flask import Flask, current_app, send_file
from flask_cors import CORS

from .config import Config

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebase-admin.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__) #, static_folder='../dist/assets')
CORS(app)
app.config.from_object(Config)

from .api import api_bp
#from .client import client_bp

app.register_blueprint(api_bp)
#app.register_blueprint(client_bp)
