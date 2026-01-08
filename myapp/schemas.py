from marshmallow import Schema, validate, ValidationError, validates_schema
from marshmallow.validate import Length
from marshmallow.fields import String, Email, Boolean
import re


def validate_password_complexity(password):
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


class RegistrationSchema(Schema):
    full_name = String(validate=Length(min=5, max=40), required=True)
    username = String(validate=Length(min=5, max=40), required=True)
    email = Email(validate=Length(max=80))
    password = String(validate=validate.And
        (
        Length(min=8, max=150),
        validate_password_complexity),
        required=True,
        load_only=True
    )
    confirm_password = String(required=True, load_only=True)

    agree_to_terms = Boolean(required=True,
                             error_messages={
                                 "required": {
                                     "message": "You must agree to the terms and conditions to continue",
                                     "code": 400
                                 }
                             })

    @validates_schema
    def confirm_passwords(self, data, **kwargs):
        """Confirm the Password inputed"""
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError({
                "confirm_password": ["Passwords are not the same"]
            })


class LoginSchema(Schema):
    email = Email(required=True)
    remember_me = Boolean()
    password = String(required=True, load_only=True)

