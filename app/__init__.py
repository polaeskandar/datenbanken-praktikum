from flask_humanize import Humanize
from flask_socketio import SocketIO
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurant.db"
app.config["SECRET_KEY"] = "543fc4a0c583435ade2e1ac8365bd132"
app.config["UPLOAD_DIRECTORY"] = "app/static/uploads/images"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
humanize = Humanize(app)

login_manager.login_view = "auth.login"
login_manager.login_message_category = "dark"


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

with app.app_context():
    db.create_all()
