from flask import current_app, jsonify
from .models import db, User
from sqlalchemy import exists, select
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token


# functions for object manipulation

def create_user(user_data):
    # User information from the form
    full_name = user_data.get("full_name").strip()
    username = user_data.get("username").strip()
    email = user_data.get("email").strip()
    password = generate_password_hash(user_data.get("password"),
                                      method="pbkdf2:sha256", salt_length=8)

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
                response_data  = {"message": f"User {full_name} has been Registered"}

                return success_response(response_data, add_access_token=True, user= new_user)
            except Exception as e:
                db.session.rollback()

                current_app.logger.error(f"Database error:"
                                         f"{str(e)}")

                response_data = {"message": f"error creating user: {str(e)}"}

                return error_response(response_data, status_code= 500)

        else:

            response_data = {"message": "Username is already taken. choose another username "}

            return error_response(response_data, status_code= 403)

    else:
        response_data = {"message":  "User already exists. Log in instead"}

        return error_response(response_data, status_code=403)


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


            return success_response( add_access_token=True, user = user)
        else:
            response_data = {"message": "User password is incorrect, Try again"}

            return error_response(response_data, status_code=403)

    else:
        response_data = {"message": "User  with that email does not exist "}
        return error_response(response_data, status_code=404)


def success_response(data= None, message= "Success", status_code= 200,
                     add_access_token = False,
                     user= None):
    """Standard Success response"""
    response = {
        "message":message,
        "data":data,
    }


    if add_access_token:

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        response.update({
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    response_data = jsonify(response)
    return response_data, status_code

def error_response(message="Error", errors=None, status_code=400):
    """Standard error response"""
    response = {
        'success': False,
        'message': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code