from factory.validators.validator import Validator

MAX_TEXT_LENGTH = 1000


class PostValidator(Validator):
    def validate(self, entity, fields, create_required_fields, create_optional_fields):
        if not super().validate(entity, fields, create_required_fields, create_optional_fields):
            return False
        if len(fields["text"]) > MAX_TEXT_LENGTH:
            return False
