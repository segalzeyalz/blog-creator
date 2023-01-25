from abc import ABC, abstractmethod
from typing import Tuple


class Validator(ABC):
    @abstractmethod
    def validate(self, entity, fields, required_fields, optional_fields) -> Tuple[bool, str]:
        entity_fields = set(entity.keys())
        required_fields = set(required_fields)
        optional_fields = set(optional_fields)

        if len(required_fields - entity_fields) > 0:
            return False, "Required field missing"

        if len(entity_fields - (required_fields | optional_fields)) > 0:
            return False, "Invalid field in entity"
        return True, ""
