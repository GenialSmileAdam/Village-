from flask_login import login_user, current_user
from flask import flash, current_app
from .models import db, User
from sqlalchemy import exists, select
from werkzeug.security import generate_password_hash, check_password_hash

# functions for object manipulation

def create_user(user_data):
    # User information from the form
    full_name = user_data.get("full_name")
    username = user_data.get("username")
    email = user_data.get("email")
    password = generate_password_hash(user_data.get("password"), method="pbkdf2:sha256", salt_length=8)


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
                return {"message": f"User {full_name} has been Registered",
                 "status": "Success",
                 "code":201}
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
