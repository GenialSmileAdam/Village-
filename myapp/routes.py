from flask import render_template, Blueprint, request, url_for, redirect, flash, current_app
from flask_login import login_user, current_user, login_required, logout_user

from .extensions import login_manager
from .models import db, User, Hobby
from .forms import RegisterForm, LoginForm
from sqlalchemy import exists, select
from werkzeug.security import generate_password_hash, check_password_hash



main_bp = Blueprint('main',__name__)
login_manager.login_view = "main.login"


# Load a user
@login_manager.user_loader
def load_user(user_id):
    return  db.session.scalar(select(User).where(User.id == user_id) )


# ---------Main Routes-------------
@main_bp.route("/")
def home():
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






# functions for object manipulation

def create_user(form):
    # User information from the form
    full_name = form.full_name.data
    username = form.username.data
    email = form.email.data
    password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)


    user_exists = db.session.query(exists().where((User.email == email))).scalar()
    username_taken = db.session.query(exists().where((User.username == username))).scalar()

    # check if user exists in the database
    if not user_exists:
        # Check if username is taken
        if not username_taken:
            try:
                new_user = User(
                    full_name = full_name,#type:ignore
                    username = username,#type:ignore
                    email = email,#type:ignore
                    password = password)#type:ignore

                db.session.add(new_user)
                db.session.commit()
                flash(f"Registration Successful. Welcome to Village {full_name}")
                login_user(new_user, remember=True)
                flash(f"User {current_user.full_name} is logged in")
                return "home"
            except Exception as e:
                db.session.rollback()
                flash(f"error creating user: {str(e)}")
                current_app.logger.error(f"Database error:"
                                 f"{str(e)}")
        else:
            flash("Username is already taken. choose another username ")
            return "signup"
    else:
        flash("User already exists. Log in instead ")
        return "login"

def confirm_login(form):
    # Get user data
    password = form.password.data
    email = form.email.data
    remember_me = form.remember_me.data
    print(remember_me)
    # check if user exists in database
    user_exists = db.session.query(exists().where((User.email == email))).scalar()

    if user_exists:
        user = db.session.scalar(select(User).where(User.email == email))

        if check_password_hash(user.password, password):
            if remember_me:
                login_user(user, remember=True)
                flash(f"User {current_user.full_name} is logged in")
                return True
            else:
                login_user(user)
                flash(f"User {current_user.full_name} is logged in")
                return True
        else:
            flash("User password is incorrect, Try again")
            return False

    else:
        flash("User  with that email does not exist ")
        return False
