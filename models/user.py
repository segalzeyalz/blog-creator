from factory.adapters.adapter import Adapter
from models.model import AbstractModel


class User(AbstractModel):
    def __init__(self, validator, db, user_adapter: Adapter):
        super().__init__(validator, db, user_adapter)

        self.collection_name = 'users'

        self.fields = {
            "email": "string",
            "password": "string",
            "posts": "array",
            "created": "datetime",
            "lastLogin": "datetime",
            "sessionId": "string",
        }

        self.create_required_fields = ["email", "password"]
        self.update_required_fields = ["email"]
        self.update_optional_fields = ["lastLogin", "sessionId", "password"]
