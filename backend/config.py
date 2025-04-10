import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Secret key for Flask app (used for session management, etc.)
    SECRET_KEY = os.getenv('SECRET_KEY')

    # MongoDB configuration
    MONGO_URI = os.getenv('MONGO_URI')  # MongoDB connection string

    # Disable SQLAlchemy track modifications (not needed for MongoDB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Auth0-related configurations
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    API_IDENTIFIER = os.getenv('API_IDENTIFIER')
    FRONTEND_URL = os.getenv('FRONTEND_URL')