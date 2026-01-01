from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login  import LoginManager


class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
csrf = CSRFProtect()
login_manager = LoginManager()

