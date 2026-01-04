from dns.e164 import query
from flask import render_template, Blueprint, request, url_for, redirect, flash, current_app, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from .extensions import login_manager
from .models import db, User, Hobby
from .forms import RegisterForm, LoginForm
from sqlalchemy import exists, select
from .functions import create_user, confirm_login
from .schemas import UserSchema, ValidationError
from pprint import pprint

main_bp = Blueprint('main',__name__)
api_bp = Blueprint("api",__name__,url_prefix="/api")
login_manager.login_view = "main.login"


# Load a user
@login_manager.user_loader
def load_user(user_id):
    return  db.session.scalar(select(User).where(User.id == user_id) )


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

@main_bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        try:
            if confirm_login(form):
                # if the login is successful
                return redirect(url_for("main.home"))
            else:
                # if the login is Unsuccessful
                return redirect(url_for("main.login"))
        except Exception as e:
            flash("An error occurred. Please try again.")
            current_app.logger.error(f"Login error: {str(e)}")
            return render_template("login.html", form=form)


    return render_template("login.html", form= form)


@main_bp.route("/sign_up", methods= ["GET", "POST"])
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


    return render_template("sign_up.html", form= form)

@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("User has been logged out")
    return redirect(url_for("main.home"))

# -------------API Routes -------------------

@api_bp.route("/register",methods= ["POST"])
def register():
    user_data = request.get_json()
    pprint(user_data)
    # Debug: Print exact values with repr() to see hidden characters
    # print("DEBUG - Raw JSON received:", user_data)
    # print(f"DEBUG - password: '{user_data.get('password')}' (type: {type(user_data.get('password'))})")
    # print(f"DEBUG - confirm_password: '{user_data.get('confirm_password')}' (type: {type(user_data.get('confirm_password'))})")
    # print(f"DEBUG - Are they equal? {user_data.get('password') == user_data.get('confirm_password')}")
    # print(f"DEBUG - Are they identical? {user_data.get('password') is user_data.get('confirm_password')}")

    schema = UserSchema()

    try:
        user_data = schema.load(user_data)
    except ValidationError as err:
        return jsonify(errors =err.messages,
                       valid_data = err.valid_data), 400
    else:
        message = create_user(user_data)

        return jsonify(data = user_data,
                       message= message), message["code"]



