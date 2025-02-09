from app import app
from .auth_routes import auth_routes
from .index_routes import index_routes
from .admin_routes import admin_routes
from .cart_routes import cart_routes
from .balance_routes import balance_routes
from .profile_routes import profile_routes

app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(index_routes, url_prefix="/")
app.register_blueprint(admin_routes, url_prefix="/admin")
app.register_blueprint(cart_routes)
app.register_blueprint(balance_routes, url_prefix="/balance")
app.register_blueprint(profile_routes, url_prefix="/profile")
