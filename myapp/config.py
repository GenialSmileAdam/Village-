import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

basedir= Path(__file__).parent.absolute()


class Config:
    """Base Configuration"""
    # Security
    SECRET_KEY = secrets.token_hex()
    DEBUG = os.environ.get('FLASK_ENV') == 'development'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    SESSION_COOKIE_SECURE = not DEBUG
    SESSION_COOKIE_HTTPONLY = True

    # File uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #16MB
    UPLOAD_FOLDER = basedir/"uploads"

    # Cookies
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = True

    # App settings
    APP_NAME = "My Flask App"

class DevelopmentConfig(Config):
    """Development settings"""
    DEBUG = True
    SQLALCHEMY_ECHO = True #Show SQL Queries

class ProductionConfig(Config):
    """Production settings"""
    Debug=False


    SQLALCHEMY_DATABASE_URI =  os.environ.get("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL is required for production")


    # Require HTTPS
    SESSION_COOKIE_SECURE = True


# Easy access
config = {
    "development": DevelopmentConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}



