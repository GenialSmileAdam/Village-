from __future__ import annotations
from flask import Blueprint, request, jsonify
from .models import db, User
from sqlalchemy import  select
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
    return str(user.id)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = int(jwt_data["sub"])
    return db.session.scalar(select(User).where(User.id == identity))


# this callback refreshes any token within 30 minutes of
# expiring
@api_bp.after_request
def refresh_expiring_jwt(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


# -------------API Routes -------------------

@api_bp.route("/register", methods=["POST"])
@limiter.limit("1/second")
def register():
    user_data = request.get_json()
    pprint(user_data)
    # Debug: Print exact values with repr() to see hidden characters
    # print("DEBUG - Raw JSON received:", user_data)
    # print(f"DEBUG - password: '{user_data.get('password')}' (type: {type(user_data.get('password'))})")
    # print(f"DEBUG - confirm_password: '{user_data.get('confirm_password')}' (type: {type(user_data.get('confirm_password'))})")
    # print(f"DEBUG - Are they equal? {user_data.get('password') == user_data.get('confirm_password')}")
    # print(f"DEBUG - Are they identical? {user_data.get('password') is user_data.get('confirm_password')}")

    schema = RegistrationSchema()

    try:
        validated_json_data = schema.load(user_data)
    except ValidationError as err:
        return jsonify(errors=err.messages,
                       valid_data=err.valid_data), 400
    else:
        registration_message = create_user(validated_json_data)

        # if registration is Successful
        if registration_message["code"] == 201:

             return confirm_login(validated_json_data)
        else:

            return success_response(registration_message)


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
        db.session.execute("SELECT 1")

        # Check if database has at least one user table (optional)
        # user_count = db.session.scalar(select(db.func.count(User.id)))

        return jsonify({
            "status": "healthy",
            "service": "auth-api",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "uptime": "N/A"  # You could add uptime tracking later
        }), 200

    except Exception as e:
        # Log the error (consider adding proper logging)
        # current_app.logger.error(f"Health check failed: {str(e)}")

        return jsonify({
            "status": "unhealthy",
            "service": "auth-api",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "disconnected",
            "error": "Database connection failed"  # Generic message for security
        }), 503  # 503 Service Unavailable