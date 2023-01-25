from factory.adapters.adapter import Adapter
from factory.validators.validator import Validator
from models.model import AbstractModel


class Post(AbstractModel):
    def __init__(self, validator: Validator, db, adapter: Adapter):
        super().__init__(validator, db, adapter)

        self.collection_name = 'posts'

        self.fields = {
            "postId": "string",
            "title": "string",
            "text": "string",
            "created": "datetime",
            "updated": "datetime",
            "writtenByUserId": "string",
            "likes": "object",
        }

        self.create_optional_fields = {}

        self.create_required_fields = ["postId", "text"]
        self.update_required_fields = ["postId"]

    def __repr__(self):
        return f"Post({self.fields['title']})"
