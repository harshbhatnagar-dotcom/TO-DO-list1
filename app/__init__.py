from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Creating database globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database with app
    db.init_app(app)
   

    # Register Blueprints
    from app.routes.auth import auth_bp  # ✅ fixed name from `auth_pb` to `auth_bp`
    from app.routes.tasks import tasks_bp  # ✅ make sure tasks_bp is defined in tasks.py

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)  # prefix for task routes

    return app
