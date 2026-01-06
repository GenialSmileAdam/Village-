from flask import render_template, Blueprint, request, url_for, redirect, flash, current_app, jsonify
# from flask_login import login_user, current_user, login_required, logout_user
from .extensions import login_manager
from .models import db, User, Hobby
from .forms import RegisterForm, LoginForm
from sqlalchemy import exists, select
from .functions import create_user, confirm_login
from .schemas import RegistrationSchema, ValidationError, LoginSchema
from pprint import pprint
from flask_jwt_extended import (jwt_required, get_jwt_identity, current_user, get_jwt,
                                create_access_token, set_access_cookies,
                                unset_jwt_cookies)
from .extensions import jwt
from datetime import timezone, timedelta, datetime

main_bp = Blueprint('main', __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")
login_manager.login_view = "main.login"


# Load a user
@login_manager.user_loader
def load_user(user_id):
    return db.session.scalar(select(User).where(User.id == user_id))


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


# ---------Main Routes-------------
@main_bp.route("/")
def home():
    # user = db.session.scalar(select(User).where(User.id == 1))
    # schema = UserSchema()
    # result = schema.dump(user)
    # pprint(result)
    return render_template("index.html")


@main_bp.route("/chat")
def chat():
    return render_template("chat.html")


# @main_bp.route("/login", methods=["POST", "GET"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#
#         try:
#             if confirm_login(form):
#                 # if the login is successful
#                 return redirect(url_for("main.home"))
#             else:
#                 # if the login is Unsuccessful
#                 return redirect(url_for("main.login"))
#         except Exception as e:
#             flash("An error occurred. Please try again.")
#             current_app.logger.error(f"Login error: {str(e)}")
#             return render_template("login.html", form=form)
#
#     return render_template("login.html", form=form)


@main_bp.route("/sign_up", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user_redirect = create_user(form)

            return redirect((url_for(f"main.{user_redirect}")))


        except Exception as e:
            flash("An error occurred. Please try again.")
            current_app.logger.error(f"Sign up error: {str(e)}")
            return render_template("sign_up.html", form=form)

    return render_template("sign_up.html", form=form)


# @main_bp.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("User has been logged out")
#     return redirect(url_for("main.home"))


# -------------API Routes -------------------

@api_bp.route("/register", methods=["POST"])
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
            response = confirm_login(validated_json_data)


            return response, registration_message["code"]
        else:

            return registration_message, registration_message["code"]


@api_bp.route("/login", methods=["POST"])
def login():
    user_data = request.get_json()
    pprint(user_data)

    schema = LoginSchema()

    try:
        validated_json_data = schema.load(user_data)
    except ValidationError as err:

        return jsonify(errors=err.messages,
                       valid_data=err.valid_data), 400
    else:
        # Confirm login and get response message
        response = confirm_login(validated_json_data)

        return response, response["code"]


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
