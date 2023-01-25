import unittest

from factory.validators.user_validator import UserValidator


class TestUserValidator(unittest.TestCase):
    def setUp(self):
        self.user_validator = UserValidator()

    def test_validate_when_password_is_short(self):
        should_be_failure = self.user_validator.validate({"email": "lala@la.com", "password": "123456"}, {}, {}, {})
        self.assertEqual(should_be_failure[0], False)
        self.assertEqual(should_be_failure[1], "short password")

    def test_is_valid_email(self):
        should_fail = self.user_validator.is_valid_email('dsdfsdf')
        should_succeed = self.user_validator.is_valid_email('dsdfsdf@abc.com')
        self.assertEqual(should_fail, False)
        self.assertEqual(should_succeed, True)


if __name__ == '__main__':
    unittest.main()
