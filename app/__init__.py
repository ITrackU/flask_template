from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    csrf.init_app(app)
    db.init_app(app)

    # Import and register routes
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    
    return app
