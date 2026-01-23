from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()


class Base(DeclarativeBase):
    pass

limiter = Limiter(get_remote_address,
                  default_limits=["200 per day", "50 per hour"],
                  )
db = SQLAlchemy(model_class=Base)
jwt = JWTManager()

if os.environ.get("FLASK_ENV") == "development":
    # Development: allow everything from localhost
    cors = CORS(
        origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        supports_credentials=True
    )
else:
    # Production: strict configuration
    cors = CORS(
        origins=["https://yourdomain.com"],
        methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
        supports_credentials=True,
        max_age=3600
    )


# CENTRALIZED LOGGER

os.makedirs("logs", exist_ok=True)   # change 3: ensure logs folder exists

logger = logging.getLogger("village_app")  # change 4: create named logger
logger.setLevel(logging.INFO)                # change 5: default level, can be ERROR in prod

# change 6: formatter for file + console
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# change 7: console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# change 8: file handler
file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import logging   # change 1: import logging for central logger
import sys       # change 2: import sys for console output

load_dotenv()


class Base(DeclarativeBase):
    pass


# -----------------------------
# Flask Extensions
# -----------------------------
db = SQLAlchemy(model_class=Base)
jwt = JWTManager()

if os.environ.get("FLASK_ENV") == "development":
    # Development: allow everything from localhost
    cors = CORS(
        origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        supports_credentials=True
    )
else:
    # Production: strict configuration
    cors = CORS(
        origins=["https://yourdomain.com"],
        methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
        supports_credentials=True,
        max_age=3600
    )

# -----------------------------
# CENTRALIZED LOGGER
# -----------------------------
os.makedirs("logs", exist_ok=True)   # change 3: ensure logs folder exists

logger = logging.getLogger("community_app")  # change 4: create named logger
logger.setLevel(logging.INFO)                # change 5: default level, can be ERROR in prod

# change 6: formatter for file + console
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# change 7: console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# change 8: file handler
file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
