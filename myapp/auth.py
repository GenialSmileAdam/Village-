import secrets, time
from flask import session, flash
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user as flask_login_user, logout_user as flask_logout_user
from sqlalchemy import select, exists

from app.extensions import db, mail
from .models import User

# ------------------ Registration ------------------
def register_user(form):
    full_name = form.full_name.data
    username = form.username.data
    email = form.email.data
    password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)

    user_exists = db.session.query(exists().where(User.email == email)).scalar()
    if user_exists:
        flash("User already exists. Log in instead.")
        return None

    new_user = User(
        full_name=full_name,
        username=username,
        email=email,
        password=password
    )
    db.session.add(new_user)
    db.session.commit()
    flash(f"Registration successful. Welcome, {full_name}!")
    return new_user

# ------------------ Login ------------------
def login_user(form):
    email = form.email.data
    password = form.password.data

    user = db.session.scalar(select(User).where(User.email == email))
    if not user:
        flash("User with that email does not exist.")
        return False

        clear_otp_session()
        flash("Login successful!")
        return True

    flash("Invalid OTP.")
    return False

def clear_otp_session():
    """Remove OTP data from session."""
    for key in ['otp', 'otp_expiry', 'otp_attempts', 'pending_user_id']:
        session.pop(key, None)

# ------------------ Logout ------------------
def logout_user():
  #remove session and tokens
    flask_logout_user()
    clear_otp_session()
    flash("You have been logged out.")

# ------------------ OTP functions ------------------
def generate_otp():
    #6 digit otp
    return str(secrets.randbelow(1000000)).zfill(6)

def send_otp(email, otp):
    #Send OTP via SMTP using Flask-Mail.
    msg = Message("Your OTP Code", recipients=[email])
    msg.body = f"Your OTP is {otp}. It expires in 5 minutes."
    mail.send(msg)

# ------------------ Password Reset ------------------
def generate_reset_token(user):
    #Generate a secure password reset token
    token = secrets.token_urlsafe(32)
    session['reset_token'] = token
    session['reset_user_id'] = user.id
    session['reset_expiry'] = time.time() + 900  # 15 minutes expiry
    return token

def send_reset_email(user, token):
    #Send password reset email with token link.
    reset_link = f"http://localhost:5000/reset_password/{token}"
    msg = Message("Password Reset Request", recipients=[user.email])
    msg.body = f"Click the link to reset your password: {reset_link}"
    mail.send(msg)

def validate_reset_token(token):
    #Validate reset token and expiry.
    stored_token = session.get('reset_token')
    expiry = session.get('reset_expiry')
    user_id = session.get('reset_user_id')

    if stored_token == token and time.time() < expiry:
        return db.session.scalar(select(User).where(User.id == user_id))
    return None

    if not check_password_hash(user.password, password):
        flash("Incorrect password.")
        return False

    # Generate and send OTP
    otp = generate_otp()
    send_otp(user.email, otp)
    session['otp'] = otp
    session['otp_expiry'] = time.time() + 300  # 5 minutes expiry
    session['otp_attempts'] = 0
    session['pending_user_id'] = user.id
    flash("OTP sent to your email.")
    return True

def validate_otp(input_otp):
    stored_otp = session.get('otp')
    expiry = session.get('otp_expiry')
    attempts = session.get('otp_attempts', 0)

    if attempts >= 5:
        flash("Too many failed attempts. Please log in again.")
        clear_otp_session()
        return False

    session['otp_attempts'] = attempts + 1

    if not stored_otp or not expiry or time.time() > expiry:
        flash("OTP expired. Please log in again.")
        clear_otp_session()
        return False

    if input_otp == stored_otp:
        # OTP valid → log user in
        user_id = session.get('pending_user_id')
        user = db.session.scalar(select(User).where(User.id == user_id))
        flask_login_user(user)