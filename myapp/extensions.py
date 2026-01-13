from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
jwt = JWTManager()

if os.environ.get("FLASK_ENV") == "development":
    # Development: allow everything from localhost
    cors = CORS(
                origins=["http://localhost:5173", "http://127.0.0.1:5000"],
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