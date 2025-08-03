# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

# Initialize the database and login manager
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'  # Redirect if user is not logged in

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)
    
    # Configuration settings
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production!
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/jobportal.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Inject current datetime globally in templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now}

    # Register routes blueprint
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Create tables if not present
    with app.app_context():
        db.create_all()

    return app
