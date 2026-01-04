from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# ---------------- Register Form ----------------
class RegisterForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=70)],
        render_kw={"placeholder": "Your full name"}
    )
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=50)]
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(),
                    EqualTo("password", message="Passwords must match")]
    )
    agree_to_terms = BooleanField(
        "I agree to the Terms of Service and Privacy Policy",
        validators=[DataRequired(message="You must agree to the terms and conditions to continue")]
    )
    submit = SubmitField("Create Account")

# ---------------- Login Form ----------------
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")

# ---------------- OTP Form ----------------
# change1: moved OTPForm out of LoginForm (was incorrectly nested)
class OTPForm(FlaskForm):
    otp = StringField("OTP", validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Verify OTP")

# ---------------- Reset Password Form ----------------
class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")]
    )
    submit = SubmitField("Reset Password")
