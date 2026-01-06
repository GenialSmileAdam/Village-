from flask import flash, current_app, jsonify
from .models import db, User
from sqlalchemy import exists, select
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies

# functions for object manipulation

def create_user(user_data):
    # User information from the form
    full_name = user_data.get("full_name").strip()
    username = user_data.get("username").strip()
    email = user_data.get("email").strip()
    password = generate_password_hash(user_data.get("password"), method="pbkdf2:sha256", salt_length=8)

    user_exists = db.session.query(exists().where((User.email == email))).scalar()
    username_taken = db.session.query(exists().where((User.username == username))).scalar()

    # check if user exists in the database
    if not user_exists:
        # Check if username is taken
        if not username_taken:
            try:
                new_user = User(
                    full_name=full_name,  # type:ignore
                    username=username,  # type:ignore
                    email=email,  # type:ignore
                    password=password)  # type:ignore

                db.session.add(new_user)
                db.session.commit()
                return {"message": f"User {full_name} has been Registered",
                        "status": "Success",
                        "code": 201}
            except Exception as e:
                db.session.rollback()

                current_app.logger.error(f"Database error:"
                                         f"{str(e)}")
                return {"message": f"error creating user: {str(e)}",
                        "status": "error",
                        "code": 500}

        else:

            return {"message": "Username is already taken. choose another username ",
                    "status": "error",
                    "code": 403}

    else:
        return {"message": "User already exists. Log in instead",
                "status": "error",
                "code": 403}


def confirm_login(user_data):
    # Get user data
    password = user_data.get("password").strip()
    email = user_data.get("email").strip()
    remember_me = user_data.get("remember_me")

    # check if user exists in database
    email_exists = db.session.query(exists().where((User.email == email))).scalar()

    if email_exists:
        user = db.session.scalar(select(User).where(User.email == email))

        if check_password_hash(user.password, password):

            access_token = create_access_token(identity=user)

            response = jsonify(
                {"message": f"User {user.full_name} has been logged in",
                    "Access_token": access_token,
                    "status": "Success",
                    "code": 200}
            )

            set_access_cookies(response, access_token)

            return response
        else:
            return {"message": "User password is incorrect, Try again",
                        "status": "error",
                        "code": 403}

    else:
        return {"message": "User  with that email does not exist ",
                        "status": "error",
                        "code": 404}
