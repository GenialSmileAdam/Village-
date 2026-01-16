import os
from flask import Flask
from .extensions import db, cors, jwt, logger   # change 1: import centralized logger
from .config import config
from dotenv import load_dotenv
from .commands import init_db_command, create_admin_command

load_dotenv()


def create_app(config_name=None):
    """Create Flask Application"""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    # Register CLI commands
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_command)

    # Register routes/blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp)

    # Attach centralized logger to app.logger
    app.logger = logger   # change 2: now app.logger uses the central logger

    return app

# ------------------------------
# Optional: remove old setup_logging # ------------------------------
# def setup_logging(app):
#     """Minimal setup for Vercel"""
#     import logging
#     import sys
#     os.makedirs("logs", exist_ok=True)
#     handler = logging.StreamHandler(sys.stdout)
#     handler.setFormatter(
#         logging.Formatter('%(levelname)s: %(message)s')
#     )
#     app.logger.handlers = [handler]
#     app.logger.setLevel(logging.INFO)

#
# def _init_extensions(app):
#     """Initialize Flask extensions with the app"""
#
#     # initialize database
#     db.init_app(app)
#
#     # initialize login manager
#
#     # import models after db is initialized
#     from .models import User, Hobby, Village, Location
#
#     # setup user loader for Flask-login
#
#
# def _register_blueprints(app):
#     """Register all blueprints/routes"""
#     from .routes import main_bp
#
#
#     app.register_blueprint(main_bp)
#
# def _add_shell_context(app):
#     """Add objects to Flask Shell context"""
#     from .extensions import db
#     from .models import User, Hobby, Village, Location
#
#     @app.shell_context_processors
#     def make_shell_context():
#         return {
#             'app':app,
#             'db':db,
#             'User':User,
#             "Hobby":Hobby,
#             "Village":Village,
#              "Location": Location
#         }