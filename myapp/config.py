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
    SECRET_KEY =  os.environ.get('SECRET_KEY',secrets.token_hex(32))
    DEBUG = os.environ.get('FLASK_ENV') == 'development'

    # JWT TOKEN
    JWT_SECRET_KEY =os.environ.get('JWT_SECRET_KEY',secrets.token_hex(32))
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours= 5)
    JWT_COOKIE_CSRF_PROTECT = True


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
    JWT_COOKIE_SECURE = True
    RATELIMIT_STORAGE_URI = "memory://"  # Use memory for development


class ProductionConfig(Config):
    """Production settings"""
    DEBUG=False
    TESTING  =False

    # SECURITY
    SECRET_KEY = os.environ['SECRET_KEY']  # Must be set
    SESSION_COOKIE_SECURE = True  # HTTPS only
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # JWT with cookies
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True

    # CORS - restrict to your frontend
    # CORS_ORIGINS = ['https://yourdomain.com']

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



