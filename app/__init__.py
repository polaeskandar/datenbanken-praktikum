from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurant.db"
app.config["SECRET_KEY"] = "543fc4a0c583435ade2e1ac8365bd132"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# IMPORTING ROUTES
from app.routes.index_routes import index_routes
from app.routes.auth_routes import auth_routes

app.register_blueprint(index_routes, url_prefix="/")
app.register_blueprint(auth_routes, url_prefix="/auth")

# IMPORTING MODELS
from app.models import *

with app.app_context():
    db.create_all()
