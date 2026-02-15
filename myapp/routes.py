from __future__ import annotations
from flask import Blueprint, request, jsonify, current_app
from .models import db, User
from sqlalchemy import  select, text
from .functions import create_user, confirm_login
from .schemas import RegistrationSchema, ValidationError, LoginSchema
from pprint import pprint
from flask_jwt_extended import (jwt_required, get_jwt_identity, current_user, get_jwt,
                                create_access_token, set_access_cookies,
                                unset_jwt_cookies)
from .extensions import jwt, limiter
from datetime import timezone, timedelta, datetime
from .functions import  error_response, success_response
# Blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api")


# load a user with jwt
@jwt.user_identity_loader
def user_identity_lookup(user):
    # Handle both User objects and user IDs
    if isinstance(user, User):
        return str(user.id)
    elif hasattr(user, 'id'):  # Just in case
        return str(user.id)
    else:  # It's already an ID
        return str(user)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]  # This will be the user ID as string

    # Convert string ID back to integer for query
    try:
        user_id = int(identity)
    except (ValueError, TypeError):
        # If identity isn't a number (e.g., email), handle differently
        return None

    return db.session.scalar(select(User).where(User.id == user_id))


# -------------API Routes -------------------

@api_bp.route("/register", methods=["POST"])
@limiter.limit("1/second")
def register():
    user_data = request.get_json()

    schema = RegistrationSchema()

    try:
        validated_json_data = schema.load(user_data)
    except ValidationError as err:
        return jsonify(errors=err.messages,
                       valid_data=err.valid_data), 400
    else:
        return create_user(validated_json_data)

        # # if registration is Successful
        # if registration_message["status_code"] == 200:
        #
        #      return confirm_login(validated_json_data)
        # else:
        #
        #     return success_response(registration_message)


@api_bp.route("/login", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def login():
    user_data = request.get_json()
    pprint(user_data)

    schema = LoginSchema()

    try:
        validated_json_data = schema.load(user_data)
    except ValidationError as err:
        errors = jsonify(errors=err.messages,
                       valid_data=err.valid_data)
        return error_response(errors)
    else:
        # Confirm login and get response message
        return  confirm_login(validated_json_data)


@api_bp.route("/get_user", methods=["GET"])
@jwt_required()
def get_user():
    #     Access the identity of the current user with get_jwt_identity

    return jsonify(id=current_user.id,
                   full_name=current_user.full_name,
                   username=current_user.username), 200

@api_bp.route("/logout", methods= ["GET"])
@jwt_required()
def logout():
    response = jsonify(
        {
            "msg": f"{current_user.full_name} has logged out Successfully"
        })
    unset_jwt_cookies(response)
    return response


@api_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    Checks database connectivity and basic app status.
    """
    try:
        # Check database connection
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "healthy",
            "service": "auth-api",
            "timestamp": datetime.now(),
            "database": "connected"
        }), 200

    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")

        return jsonify({
            "status": "unhealthy",
            "service": "auth-api",
            "timestamp": datetime.now(),
            "database": "disconnected",
            "error": "Database connection failed"
        }), 503

# this route refreshes access tokens
# Refresh tokens to access this route
@api_bp.route("/refresh", methods = ["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)