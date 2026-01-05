from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask import current_app

load_dotenv()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# csrf = CSRFProtect()
login_manager = LoginManager()

if os.environ.get("FLASK_ENV") == "development":
    # Development: allow everything from localhost
    cors = CORS(
                origins=["http://localhost:3000", "http://127.0.01:3000"],
                supports_credentials=True)
else:
# Production: strict configuration
    cors = CORS(
                origins=["https://yourdomain.com"],
                methods=["GET", "POST", "PUT", "DELETE"],
                allow_headers=["Content-Type", "Authorization"],
                supports_credentials=True,
                max_age=3600
                )