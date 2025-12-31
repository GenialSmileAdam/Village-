from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired,Email

# A RegisterForm to register new users

class RegisterForm(FlaskForm):
    full_name = StringField("Full Name",validators=[DataRequired()])
    username = StringField("Username" , validators=[DataRequired()])
    email = EmailField("Email" , validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    agree_to_terms = BooleanField("I agree to the Terms of Service and Privacy Policy")
    submit = SubmitField("Create Account")

# A LoginForm to login existing users
class LoginForm(FlaskForm):
    email = EmailField("Email" , validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")