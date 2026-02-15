from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import limits.storage as storage

load_dotenv()


class Base(DeclarativeBase):
    pass
limiter = Limiter(get_remote_address,
                  storage_options={"socket_connect_timeout": 30})
db = SQLAlchemy(model_class=Base)
jwt = JWTManager()

if os.environ.get("FLASK_ENV") == "development":
    # Development: allow everything from localhost
    cors = CORS(
                origins=["http://localhost:5173", "http://172.21.0.1:5173/"])
else:
# Production: strict configuration
    cors = CORS(
                origins=["https://yourdomain.com"],
                methods=["GET", "POST", "PUT", "DELETE"],
                allow_headers=["Content-Type", "Authorization"],
                supports_credentials=True,
                max_age=3600
                )