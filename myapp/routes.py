from flask import Flask, render_template, Blueprint
from .models import db, User, Hobby

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


@main_bp.route("/sign_up")
def signup():
    return render_template("sign_up.html")