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
    from .extensions import db, cors, jwt, limiter, get_redis_client

    db.init_app(app)
    cors.init_app(app,
        origins=app.config['CORS_ORIGINS'],
        allow_headers=app.config['CORS_ALLOW_HEADERS'],
        supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'],
        methods=app.config.get('CORS_METHODS', ["GET", "POST", "PUT", "DELETE"]))

    jwt.init_app(app)
    limiter.init_app(app)
    with app.app_context():
        redis_client = get_redis_client()


        from . import extensions as extensions_module
        extensions_module.jwt_redis_blocklist = redis_client

        if app.config['RATELIMIT_STORAGE_URI'] != 'memory://':
            limiter.storage_uri = app.config['RATELIMIT_STORAGE_URI']

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