import click
from sqlalchemy.util import create_proxy_methods
from .models import db, User
from sqlalchemy import exists
from werkzeug.security import generate_password_hash
from random import randint

from .extensions import logger  # change 1: import central logger


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables"""
    try:  # change 2: wrap in try/except for logging
        db.create_all()
        logger.info("Database Initialized")  # change 3: log success
        click.echo("Database Initialized")
    except Exception as e:
        logger.exception("Database initialization failed")  # change 3: log failure
        click.echo(f"Database initialization failed: {str(e)}")


@click.command("create-admin")
@click.option("--email", prompt=True)
@click.password_option(
    "--password",
    prompt=True,
    hide_input=False,
    confirmation_prompt=True,
    prompt_required=True
)
@click.option("--full_name", prompt=True)
def create_admin_command(email, password, full_name):
    """Create Admin User"""
    try:  # change 2: wrap in try/except for logging
        # Admin details
        admin_password = generate_password_hash(
            password=password,
            method="pbkdf2:sha256",
            salt_length=8
        )
        username = f"Admin{randint(1000, 9999)}"

        user_exists = db.session.query(exists().where(User.email == email)).scalar()
        username_taken = db.session.query(exists().where(User.username == username)).scalar()

        # check if user exists in the database
        if not user_exists and not username_taken:
            admin = User(
                email=email,
                password=admin_password,
                is_admin=True,
                username=username,
                full_name=full_name
            )
            db.session.add(admin)
            db.session.commit()
            logger.info(f"Admin {admin.full_name} ({admin.username}) has been created")  # change 3: log success
            click.echo(f"Admin {admin.full_name} ({admin.username}) has been created")
        else:
            logger.warning("Admin user not created, Username or Email is in use")  # change 3: log warning
            click.echo("Admin user not created, Username or Email is in use")
    except Exception as e:
        db.session.rollback()  # change 3: rollback on error
        logger.exception("Error creating admin user")  # change 3: log exception
        click.echo(f"Error creating admin user: {str(e)}")
