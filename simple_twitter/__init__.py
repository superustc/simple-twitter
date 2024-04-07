from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple_twitter.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

socketio = SocketIO(app)
# Ensure models are imported before creating tables
# from yourapplication.models import User, Chat
# OR ensure models are imported within routes if routes import models

from simple_twitter import routes

with app.app_context():
    db.create_all()