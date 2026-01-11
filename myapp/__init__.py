import os
from flask import Flask
from .extensions import db
from .config import config
from dotenv import load_dotenv
from .commands import init_db_command, create_admin_command

load_dotenv()

def create_app(config_name=None):
    """Create Flask Application"""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    # Get project Root path
    # project_root = Path(__file__).parent.parent.absolute()

    app = Flask(__name__)

    # Setup logging
    setup_logging(app)
    #Load Configuration
    app.config.from_object(config[config_name])

    # Register commands
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_command)

    # initialize extensions
    from .extensions import db,  cors, jwt
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    # Register routes/blueprints
    from .routes import  api_bp
    app.register_blueprint(api_bp)





    return app


def setup_logging(app):
    """Minimal setup for Vercel"""
    import logging
    import sys

    # Single handler to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter('%(levelname)s: %(message)s')
    )

    app.logger.handlers = [handler]
    app.logger.setLevel(logging.INFO)
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