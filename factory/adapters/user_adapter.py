from werkzeug.security import generate_password_hash

from factory.adapters.adapter import Adapter


class UserAdapter(Adapter):
    @staticmethod
    def adapt(entity):
        entity["email"] = entity["email"].strip()
        entity["password"] = generate_password_hash(entity["password"])
