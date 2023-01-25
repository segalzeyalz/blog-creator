from typing import Tuple


class AbstractModel:
    def __init__(self, validator, db, adapter):
        self.validator = validator
        self.db = db
        self.adapter = adapter
        self.collection_name = ''

        self.fields = {}
        self.create_required_fields = []
        self.create_optional_fields = []
        self.update_required_fields = []
        self.update_optional_fields = []

    def create(self, entity) -> Tuple[bool, str]:
        try:
            is_validated, validation_msg = self.validator.validate(
                entity, self.fields, self.create_required_fields, self.create_optional_fields)
            if not is_validated:
                return False, "not validated"

            self.adapter.adapt(entity)
            self.db.insert_one(entity, self.collection_name)
            return True, ""
        except Exception as e:
            return False, "failed to proceed the post"

    def find(self, entity):
        return self.db.find(entity)

    def update(self, query, entity) -> Tuple[bool, str]:
        self.validator.validate(entity, self.fields, self.update_required_fields, self.update_optional_fields)
        self.adapter.adapt(entity)
        self.db.update_one(query, entity, True)
        return True, ''

    def delete(self, id):
        return self.db.delete(id)
