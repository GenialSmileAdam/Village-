from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import time as time_module
from datetime import timedelta
from typing import Optional, Dict, Any

load_dotenv()


class Base(DeclarativeBase):
    pass


limiter = Limiter(
    get_remote_address,
    storage_options={"socket_connect_timeout": 30}
)
db = SQLAlchemy(model_class=Base)
jwt = JWTManager()
cors = CORS()


class JWTBlocklistMock:
    """
    Complete mock for JWT blocklist functionality
    """

    def __init__(self):
        self._blocklist: Dict[str, str] = {}
        self._expiry: Dict[str, float] = {}

    def get(self, jti: str) -> Optional[str]:
        """Check if JTI is in blocklist"""
        self._clean_expired()
        return self._blocklist.get(jti)

    def set(self, key: str, value: str, **kwargs) -> bool:
        """
        Add JTI to blocklist
        Handles ex parameter for expiration
        """
        ex = kwargs.get('ex')
        if ex:
            if isinstance(ex, timedelta):
                ex_seconds = int(ex.total_seconds())
            else:
                ex_seconds = int(ex)
            return self.setex(key, ex_seconds, value)

        self._blocklist[key] = value
        return True

    def setex(self, key: str, seconds: int, value: str) -> bool:
        """Add JTI to blocklist with expiration"""
        self._blocklist[key] = value
        self._expiry[key] = time_module.time() + seconds
        return True

    def delete(self, key: str) -> int:
        """Remove JTI from blocklist"""
        if key in self._blocklist:
            del self._blocklist[key]
            if key in self._expiry:
                del self._expiry[key]
            return 1
        return 0

    def exists(self, key: str) -> int:
        """Check if key exists in blocklist"""
        self._clean_expired()
        return 1 if key in self._blocklist else 0

    def _clean_expired(self):
        """Remove expired tokens"""
        current_time = time_module.time()
        expired_keys = [
            key for key, exp_time in self._expiry.items()
            if current_time > exp_time
        ]
        for key in expired_keys:
            del self._blocklist[key]
            del self._expiry[key]


def get_redis_client():
    """Get Redis client from app config or return mock"""
    try:
        # Try to get Redis URL from environment or config
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')

        # Try to get from app config if in app context
        try:
            from flask import current_app
            redis_url = current_app.config.get('REDIS_URL', redis_url)
        except (RuntimeError, ImportError):
            # Outside app context, use env var
            pass

        if redis_url == 'redis://localhost:6379':
            # Try localhost connection
            client = redis.StrictRedis(
                host="localhost",
                port=6379,
                db=0,
                decode_responses=True,
                socket_connect_timeout=2
            )
        else:
            # Use URL from config/environment
            client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2
            )

        client.ping()  # Test connection
        print(f"✅ Redis connected successfully using {redis_url}")
        return client
    except Exception as e:
        print(f"⚠️ Redis connection failed: {e}, using mock")
        return JWTBlocklistMock()


# Initialize with mock, will be updated in create_app
jwt_redis_blocklist = JWTBlocklistMock()