import os
from flask import Flask
from .extensions import db
from .config import config
from dotenv import load_dotenv
from pathlib import Path
import click

load_dotenv()

def create_app(config_name=None):
    """Create Flask Application"""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    # Get project Root path
    project_root = Path(__file__).parent.parent.absolute()

    app = Flask(__name__,
                template_folder=project_root / "templates",
                static_folder=project_root/ "static")

    #Load Configuration
    app.config.from_object(config[config_name])

    # Register the init-db command
    @app.cli.command("init-db")
    def init_db_command():
        """Clear existing data and create new tables"""
        from .models import db

        with app.app_context():
            db.create_all()
        click.echo("Initialized the database")


    # initialize extensions
    from .extensions import db, login_manager, cors, jwt
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    # csrf.init_app(app)
    login_manager.init_app(app)

    # Register routes/blueprints
    from .routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)





    return app


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