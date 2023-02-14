import re
from better_profanity import profanity
from marshmallow import Schema, fields, validate, validates, ValidationError

class PostSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=5, max=100))
    text = fields.Str(required=True, validate=validate.Length(min=50, max=1000))
    author = fields.Email()

    @validates('title')
    @validates('text')
    def validate_title(self, text: str):
        if profanity.contains_profanity(text):
            raise ValidationError('text contains inappropriate language')

class PostUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=5, max=100))
    text = fields.Str(validate=validate.Length(min=50, max=1000))

class UserSchema(Schema):
    email = fields.Email(required=True, description='The email address of the user')
    password = fields.Str(required=True, load_only=True, description='The password of the user', validate=validate.Length(min=6))

    @validates('password')
    def validate_password_strength(self, password: str):
        if not re.search(r"[a-z]", password):
            raise ValidationError('Password must contain at least one lowercase letter')

        if not re.search(r"[A-Z]", password):
            raise ValidationError('Password must contain at least one uppercase letter')

        if not re.search(r"\d", password):
            raise ValidationError('Password must contain at least one digit')

        if not re.search(r"[!@#$%^&*()_+-={}|[\]\\:\";'<>?,./]", password):
            raise ValidationError('Password must contain at least one special character')