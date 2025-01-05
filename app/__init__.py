from os import getenv

from dotenv import load_dotenv
from flask_humanize import Humanize
from flask_socketio import SocketIO
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["UPLOAD_DIRECTORY"] = getenv("UPLOAD_DIRECTORY")

# DB CONFIGURATION
db = SQLAlchemy(app)

# BCRYPT CONFIGURATION
bcrypt = Bcrypt(app)

# LOGIN MANAGER
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
login_manager.login_message_category = "dark"

# HUMANIZE CONFIGURATION
humanize = Humanize(app)


@humanize.localeselector
def get_locale():
    return "en_US"


# IMPORTING ROUTES
from app.routes.index_routes import index_routes
from app.routes.auth_routes import auth_routes
from app.routes.admin_routes import admin_routes

app.register_blueprint(index_routes, url_prefix="/")
app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(admin_routes, url_prefix="/admin")

# IMPORTING CHANNELS
from app.channel import *

# IMPORTING MODELS
from app.models import *

# STRIPE CONFIGURATION
from app.services.balance_service import init_stripe

init_stripe()

with app.app_context():
    db.create_all()
