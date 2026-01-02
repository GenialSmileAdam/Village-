from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re


# A RegisterForm to register new users

def validate_password_complexity(form, field):
    password = field.data
    errors = []

    if len(password) < 8:
        errors.append("at least 8 characters")

    if not re.search(r'[A-Z]', password):
        errors.append("one uppercase letter")

    if not re.search(r'[a-z]', password):
        errors.append("one lowercase letter")

    if not re.search(r'\d', password):
        errors.append("one number")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("one special character (!@#$%^&* etc.)")

    if errors:
        raise ValidationError(f'Password needs: {", ".join(errors)}')


class RegisterForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=70)],
                            render_kw={"placeholder": "Your full name"})
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=50)],
                           render_kw={"placeholder": "What others see"})
    email = EmailField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Your email "})
    password = PasswordField("Password", validators=[DataRequired(),
                                                     validate_password_complexity],
                             render_kw={
                                 "placeholder": "Min 8 chars: A-Z, a-z, 0-9, special",
                                 "autocomplete": "new-password"
                             })
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),
                                                                     EqualTo("password",
                                                                             message="Passwords must match")])
    agree_to_terms = BooleanField("I agree to the Terms of Service and Privacy Policy",
                                  validators=[
                                      DataRequired(message="You must agree to the terms and conditions to continue")])
    submit = SubmitField("Create Account")


# A LoginForm to login existing users
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign In")
