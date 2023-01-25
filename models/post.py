from typing import Tuple

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
            "author": "string",
            "likes": "object",
        }

        self.create_optional_fields = {}

        self.create_required_fields = ["postId", "text", "title", "author"]
        self.update_required_fields = ["postId"]
        self.update_optional_fields = ["text", "title"]

    def update(self, query, entity) -> Tuple[bool, str]:
        # better do here validation with validators
        text = entity['text']
        title = entity['title']
        if text == '' or title == '':
            return False, 'empty fields'
        if len(title) > 1000 or len(text) > 1000:
            return False, 'text or title are too long'

        self.adapter.adapt(entity)
        self.db.update_one(query, entity, True)
        return True, ''

    def __repr__(self):
        return f"Post({self.fields['title']})"
