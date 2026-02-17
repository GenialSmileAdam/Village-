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
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is required for production")

    DEBUG = os.environ.get('FLASK_ENV') == 'development'

    # JWT TOKEN

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY is required for production")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # CORS CONFIGURATION
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = ["Content-Type", "Authorization"]
    CORS_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # File uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #16MB
    UPLOAD_FOLDER = basedir/"uploads"


    # Redis configuration
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

    # Rate limiting configuration
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    RATELIMIT_STORAGE_URI = REDIS_URL
    RATELIMIT_STRATEGY = "fixed-window"
    # App settings
    APP_NAME = "My Flask App"

class DevelopmentConfig(Config):
    """Development settings"""
    DEBUG = True
    SQLALCHEMY_ECHO = True #Show SQL Queries
    RATELIMIT_STORAGE_URI = "memory://"  # Use memory for development


class ProductionConfig(Config):
    """Production settings"""
    DEBUG=False
    TESTING  =False

    # SECURITY
    SECRET_KEY = os.environ['SECRET_KEY']  # Must be set

    # CORS - restrict to your frontend
    CORS_ORIGINS =  os.environ.get('CORS_ORIGINS')

    SQLALCHEMY_DATABASE_URI =  os.environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,  # Recycle DB connections every 5 minutes
        'pool_pre_ping': True,  # Verify connection before using
    }
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL is required for production")



# Easy access
config = {
    "development": DevelopmentConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}



