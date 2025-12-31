from flask import render_template, Blueprint, request, url_for, redirect, flash
from .models import db, User, Hobby
from .forms import RegisterForm, LoginForm
from sqlalchemy import exists
from werkzeug.security import generate_password_hash, check_password_hash



main_bp = Blueprint('main',__name__)

# ---------Main Routes-------------
@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/chat")
def chat():
    return render_template("chat.html")

@main_bp.route("/login")
def login():
    return render_template("login.html")


@main_bp.route("/sign_up", methods= ["GET", "POST"])
def signup():
    form = RegisterForm()
    print(f"Form submitted: {request.method}")  # Debug
    print(f"Form validate on submit: {form.validate_on_submit()}")  # Debug
    print(f"Form errors: {form.errors}")  # Debug

    if form.validate_on_submit():
        if create_user(form):
            return redirect(url_for("main.home"))
        else:
            return redirect(url_for("main.login"))
    return render_template("sign_up.html", form= form)


def create_user(form):
    # User information from the form
    full_name = form.full_name.data
    username = form.username.data
    email = form.email.data
    password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)


    user_exists = db.session.query(exists().where((User.email == email))).scalar()
    # check if user exists in the database
    if not user_exists:

        new_user = User(
            full_name = full_name,
            username = username,
            email = email,
            password = password)

        db.session.add(new_user)
        db.session.commit()
        flash(f"Registration Successful. Welcome to Village {full_name}")
        return True

    else:
        flash("User already exists. Log in instead ")
        return False

