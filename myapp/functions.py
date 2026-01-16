from flask import jsonify
from .models import db, User
from sqlalchemy import exists, select
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies
from .extensions import logger  # change1: centralized logger


# ---------------- Object manipulation functions ----------------

def create_user(user_data):
    """Create a new user in the database"""
    full_name = user_data.get("full_name").strip()
    username = user_data.get("username").strip()
    email = user_data.get("email").strip()
    password = generate_password_hash(user_data.get("password"),
                                     method="pbkdf2:sha256", salt_length=8)

    user_exists = db.session.query(exists().where(User.email == email)).scalar()
    username_taken = db.session.query(exists().where(User.username == username)).scalar()

    if not user_exists:
        if not username_taken:
            try:
                new_user = User(
                    full_name=full_name,  # type:ignore
                    username=username,    # type:ignore
                    email=email,          # type:ignore
                    password=password     # type:ignore
                )
                db.session.add(new_user)
                db.session.commit()
                logger.info(f"User created successfully: {email}")  # change2: log success
                return {"message": f"User {full_name} has been registered",
                        "status": "success",
                        "code": 201}
            except Exception as e:
                db.session.rollback()
                logger.exception(f"Error creating user: {email}")  # change2: log exception
                return {"message": f"Error creating user: {str(e)}",
                        "status": "error",
                        "code": 500}
        else:
            logger.warning(f"Username already taken: {username}")  # change2: log warning
            return {"message": "Username is already taken. Choose another username",
                    "status": "error",
                    "code": 403}
    else:
        logger.warning(f"User already exists: {email}")  # change2: log warning
        return {"message": "User already exists. Log in instead",
                "status": "error",
                "code": 403}


def confirm_login(user_data):
    """Authenticate user and return JWT token"""
    password = user_data.get("password").strip()
    email = user_data.get("email").strip()
    remember_me = user_data.get("remember_me")

    email_exists = db.session.query(exists().where(User.email == email)).scalar()

    if email_exists:
        user = db.session.scalar(select(User).where(User.email == email))
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user)
            response_data = {"access_token": access_token}
            logger.info(f"User login successful: {email}")  # change2: log success
            return success_response(response_data, add_access_token=True)
        else:
            logger.warning(f"Incorrect password attempt for: {email}")  # change2: log warning
            return error_response("User password is incorrect, try again", status_code=403)
    else:
        logger.warning(f"Login attempt for non-existent user: {email}")  # change2: log warning
        return error_response("User with that email does not exist", status_code=404)


# ---------------- Response helpers ----------------

def success_response(data=None, message="Success", status_code=200, add_access_token=False):
    """Standard success response"""
    response = {
        "success": True,
        "message": message,
        "data": data,
    }
    response_data = jsonify(response)
    if add_access_token:
        set_access_cookies(response_data, data["access_token"])
    return response_data, status_code


def error_response(message="Error", errors=None, status_code=400):
    """Standard error response"""
    response = {
        "success": False,
        "message": message
    }
    if errors:
        response["errors"] = errors
    return jsonify(response), status_code
