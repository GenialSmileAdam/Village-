from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import os
import smtplib
from email.message import EmailMessage

from models import db, User, OTPToken

auth_bp = Blueprint("auth", __name__)

# =========================
# CONFIG
# =========================

OTP_EXPIRY_MINUTES = 10

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# SMTP AND OTP 

def send_otp_email(to_email, otp_code, purpose):
    msg = EmailMessage()
    msg["Subject"] = "Your Verification Code"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    msg.set_content(
        f"""
Your verification code is: {otp_code}

Purpose: {purpose}
This code expires in {OTP_EXPIRY_MINUTES} minutes.

If you did not request this, ignore this email.
        """
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()    # TLS encryption
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


# REGISTER (SIGNUP)

@auth_bp.route("/api/register", methods=["POST"])
def register_user():
    data = request.json

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    password_hash = generate_password_hash(password)

    user = User(
        email=email,
        username=username,
        password_hash=password_hash,
        is_verified=False
    )

    db.session.add(user)
    db.session.commit()

    # Generate OTP
    otp_code = str(random.randint(100000, 999999))
    otp_hash = generate_password_hash(otp_code)

    otp = OTPToken(
        user_id=user.id,
        otp_hash=otp_hash,
        purpose="VERIFY_EMAIL",
        expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    )

    db.session.add(otp)
    db.session.commit()

    send_otp_email(email, otp_code, "Email Verification")

    return jsonify({"message": "OTP sent to email"}), 201

# VERIFY EMAIL OTP

@auth_bp.route("/api/verify-otp", methods=["POST"])
def verify_email_otp():
    data = request.json

    email = data.get("email")
    otp_input = data.get("otp")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    otp = OTPToken.query.filter_by(
        user_id=user.id,
        purpose="VERIFY_EMAIL",
        used=False
    ).order_by(OTPToken.created_at.desc()).first()

    if not otp:
        return jsonify({"error": "OTP not found"}), 404

    if otp.is_expired():
        return jsonify({"error": "OTP expired"}), 400

    if not check_password_hash(otp.otp_hash, otp_input):
        otp.attempts += 1
        db.session.commit()
        return jsonify({"error": "Invalid OTP"}), 400

    # Success
    otp.used = True
    user.is_verified = True

    db.session.commit()

    return jsonify({"message": "Account verified successfully"}), 200

# LOGIN

@auth_bp.route("/api/login", methods=["POST"])
def login_user():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.is_verified:
        return jsonify({"error": "Account not verified"}), 403

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200
