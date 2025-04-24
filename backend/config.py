import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # Secret key for Flask app (used for session management, etc.)
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

    # PostgreSQL configuration
    DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'chatbot')
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'Admin')

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
        f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Auth0-related configurations
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    API_IDENTIFIER = os.getenv('API_IDENTIFIER')
    FRONTEND_URL = os.getenv('FRONTEND_URL')

    # API Keys for integrations
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
