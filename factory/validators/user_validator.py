import re
from typing import Tuple

from factory.validators.validator import Validator


class UserValidator(Validator):
    def validate(self, entity, fields, required_fields, optional_fields) -> Tuple[bool, str]:
        email, password = entity.get('email', None), entity.get('password', None)
        if not email or not password:
            return False, 'missing fields'
        if len(password) < 8:
            return False, 'short password'
        if not self.is_valid_email(email):
            return False, 'invalid email'
        return True, ''

    @staticmethod
    def is_valid_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(regex, email):
            return True
        return False
