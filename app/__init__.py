from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from app.routes import routes_blueprint
import app.models as models

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurant.db"
app.config["SECRET_KEY"] = "543fc4a0c583435ade2e1ac8365bd132"
app.register_blueprint(routes_blueprint)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

with app.app_context():
    db.create_all()
