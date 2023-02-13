from marshmallow import Schema, fields

class PostSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    text = fields.Str(required=True)
    author = fields.Str()

class PostUpdateSchema(Schema):
    title = fields.Str()
    text = fields.Str()

class UserSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)