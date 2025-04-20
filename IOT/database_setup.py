
from iot_app.models import SensorData, Override
import sys
import os

from iot_app import create_app, db

def initialize_database():
    """
    Initializes the database with the current models.
    """
    app = create_app()
    with app.app_context():
        db.create_all()  # Creates tables for all models
        print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
