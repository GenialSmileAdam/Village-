import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

basedir = Path(__file__).parent.absolute()


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
    SESSION_PROTECTION = "strong"   # change1: add session protection for Flask-Login

    # File uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = basedir / "uploads"

    # Cookies
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = True

    # Mail settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")   # change2: add mail server
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))               # change3: add mail port
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "1"]   # change4: TLS toggle
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() in ["true", "1"]  # change5: SSL toggle
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")                 # change6: mail username
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")                 # change7: mail password
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@example.com")  # change8: default sender

    # CSRF
    WTF_CSRF_ENABLED = True          # change9: enable CSRF protection
    WTF_CSRF_TIME_LIMIT = None       # change10: disable CSRF expiry (or set seconds)

    # App settings
    APP_NAME = "My Flask App"
    APP_URL = os.environ.get("APP_URL", "http://localhost:5000")   # change11: add APP_URL for reset links


class DevelopmentConfig(Config):
    """Development settings"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Show SQL Queries


class ProductionConfig(Config):
    """Production settings"""
    DEBUG = False   # change12: fix capitalization of DEBUG

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL is required for production")

    # Require HTTPS
    SESSION_COOKIE_SECURE = True

# Easy access
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
