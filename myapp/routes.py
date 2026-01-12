from flask import Blueprint, request, jsonify
from .models import db, User
from sqlalchemy import select
from .functions import create_user, confirm_login, error_response, success_response
from .schemas import RegistrationSchema, ValidationError, LoginSchema
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, current_user, get_jwt,
    create_access_token, set_access_cookies, unset_jwt_cookies
)
from .extensions import jwt, logger  # change1: use central logger
from datetime import timezone, timedelta, datetime
from pprint import pprint

# Blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api")


# ---------------- JWT User Loaders ----------------

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = int(jwt_data["sub"])
    return db.session.scalar(select(User).where(User.id == identity))


# refresh JWT if expiring in 30 minutes
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
        # No valid JWT, just return original response
        logger.debug("No JWT found to refresh")  # change2: log JWT debug
        return response


# ---------------- API Routes -------------------

@api_bp.route("/register", methods=["POST"])
def register():
    user_data = request.get_json()
    pprint(user_data)
    logger.info(f"Register request data: {user_data}")  # change3: log incoming request

    schema = RegistrationSchema()

    try:
        validated_json_data = schema.load(user_data)
    except ValidationError as err:
        logger.warning(f"Validation errors: {err.messages}")  # change3: log validation errors
        return jsonify(errors=err.messages, valid_data=err.valid_data), 400
    else:
        registration_message = create_user(validated_json_data)

        if registration_message["code"] == 201:
            logger.info(f"User registered successfully: {validated_json_data.get('email')}")  # change3
            return confirm_login(validated_json_data)
        else:
            logger.warning(f"Registration failed: {registration_message}")  # change3
            return error_response(registration_message["message"], status_code=registration_message["code"])


@api_bp.route("/login", methods=["POST"])
def login():
    user_data = request.get_json()
    pprint(user_data)
    logger.info(f"Login attempt: {user_data.get('email')}")  # change3

    schema = LoginSchema()

    try:
        validated_json_data = schema.load(user_data)
    except ValidationError as err:
        logger.warning(f"Login validation failed: {err.messages}")  # change3
        return error_response(err.messages, status_code=400)
    else:
        result = confirm_login(validated_json_data)
        logger.info(f"Login result: {result}")  # change3
        return result


@api_bp.route("/get_user", methods=["GET"])
@jwt_required()
def get_user():
    logger.info(f"Get user info: {current_user.username}")  # change3
    return jsonify(
        id=current_user.id,
        full_name=current_user.full_name,
        username=current_user.username
    ), 200


@api_bp.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    logger.info(f"User logged out: {current_user.username}")  # change3
    response = jsonify({"msg": f"{current_user.full_name} has logged out successfully"})
    unset_jwt_cookies(response)
    return response
