from typing import Tuple

from factory.adapters.adapter import Adapter
from factory.validators.validator import Validator
from models.model import AbstractModel


class PostModel(AbstractModel):
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

    def update(self, query: dict, by_params: dict) -> Tuple[bool, str]:
        try:
            by_param_update_query = self.adapter.adapt(by_params)
            self.db.update_one(query, by_param_update_query)
            return True, ''
        except Exception as e:
            return False, str(e)

    def __repr__(self):
        return f"Post({self.fields['title']})"
