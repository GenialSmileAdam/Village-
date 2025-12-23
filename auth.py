from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import random

# Blueprint for auth routes
auth_bp = Blueprint("auth", __name__)

# In-memory storage (temporary )
users_db = {}
otp_store = {}


# Register user + send OTP

@auth_bp.route("/api/register", methods=["POST"])
def register_user():
    data = request.json

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if email in users_db:
        return jsonify({"error": "User already exists"}), 409

    # Hash password
    password_hash = generate_password_hash(password)

    # Generate OTP
    otp_code = random.randint(100000, 999999)

    # Store user temporarily
    users_db[email] = {
        "username": username,
        "password": password_hash,
        "is_verified": False
    }

    # Store OTP temporarily
    otp_store[email] = otp_code

 #tempoary
    print(f"OTP for {email}: {otp_code}")

    return jsonify({"message": "OTP sent to email"}), 201

# Verify OTP
@auth_bp.route("/api/verify-otp", methods=["POST"])
def verify_user_otp():
    data = request.json

    email = data.get("email")
    otp = data.get("otp")

    if email not in otp_store:
        return jsonify({"error": "OTP not found"}), 404

    if int(otp) != otp_store[email]:
        return jsonify({"error": "Invalid OTP"}), 400

    # Mark user as verified
    users_db[email]["is_verified"] = True

    # Remove OTP
    otp_store.pop(email)

    return jsonify({"message": "Account verified successfully"}), 200

login 

@auth_bp.route("/api/login", methods=["POST"])
def login_user():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    user = users_db.get(email)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user["is_verified"]:
        return jsonify({"error": "Account not verified"}), 403

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200
