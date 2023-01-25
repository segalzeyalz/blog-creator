from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, entity, fields, required_fields, optional_fields):
        entity_fields = set(entity.keys())
        required_fields = set(required_fields)
        optional_fields = set(optional_fields)

        if len(required_fields - entity_fields) > 0:
            raise ValueError("Required field missing")

        if len(entity_fields - (required_fields | optional_fields)) > 0:
            raise ValueError("Invalid field in entity")