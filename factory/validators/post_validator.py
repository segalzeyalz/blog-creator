from typing import Tuple

from factory.validators.validator import Validator

MAX_TEXT_LENGTH = 1000


class PostValidator(Validator):
    def validate(self, entity, fields, create_required_fields, create_optional_fields) -> Tuple[bool, str]:
        try:
            is_generally_validated = super().validate(
                entity, fields, create_required_fields, create_optional_fields)
            if not is_generally_validated:
                return False, "fields are not as expected"
            if len(fields["text"]) > MAX_TEXT_LENGTH:
                return False, "Text is too long"
            return True, ""
        except Exception as e:
            return False, str(e)
