from flask import render_template, Blueprint, request, url_for, redirect, flash
from .models import db, User, Hobby
from .forms import RegisterForm, LoginForm



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
        full_name = form.full_name.data
        print(full_name)
        flash(f"User: {full_name} has successfully signed in!")
        return redirect(url_for("main.home"))
    return render_template("sign_up.html", form= form)