# flask-app
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# database
import os
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lines.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# session
from flask import session
from os import urandom

app.secret_key = urandom(32)

# general functionality
from application import views

from application.lines import models

from application.auth.admin import views
from application.auth.admin import forms

db.create_all()
