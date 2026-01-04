from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask_login import login_required

from .extensions import login_manager
from .models import db, User
from .forms import RegisterForm, LoginForm, OTPForm   #change1: import OTPForm
from sqlalchemy import select
from .auth import register_user, login_user, validate_otp, logout_user #change2 import auth 

main_bp = Blueprint('main', __name__)
login_manager.login_view = "main.login"

# Load a user
@login_manager.user_loader
def load_user(user_id):
    return db.session.scalar(select(User).where(User.id == user_id))

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
        if login_user(form):   #change3: call auth.login_user(form) instead of confirm_login
            return redirect(url_for("main.verify_otp"))   #change4: redirect to OTP verification
        else:
            return redirect(url_for("main.login"))
    return render_template("login.html", form=form)

@main_bp.route("/verify_otp", methods=["GET", "POST"])   #change5: new route for OTP verification
def verify_otp():
    form = OTPForm()
    if form.validate_on_submit():
        if validate_otp(form.otp.data):   #change6: call auth.validate_otp
            return redirect(url_for("main.home"))
    return render_template("verify_otp.html", form=form)

@main_bp.route("/sign_up", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if register_user(form):   #change7: call auth.register_user(form) instead of local create_user
            return redirect(url_for("main.home"))
        else:
            return redirect(url_for("main.login"))
    return render_template("sign_up.html", form=form)

@main_bp.route("/logout")
@login_required
def logout():
    logout_user()   #change8: call auth.logout_user instead of flask_logout_user directly
    flash("User has been logged out")
    return redirect(url_for("main.home"))

#change9: removed local create_user and confirm_login functions, since they now live in auth.py
