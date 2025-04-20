from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Initialize the SQLAlchemy object without tying it to the app yet
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints or routes
    from .routes import main
    app.register_blueprint(main)

    return app
