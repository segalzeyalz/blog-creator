from marshmallow import Schema, fields

class PostSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    text = fields.Str(required=True)
    author = fields.Str()

class PostUpdateSchema(Schema):
    title = fields.Str()
    text = fields.Str()