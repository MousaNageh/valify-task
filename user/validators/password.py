import re
from rest_framework.exceptions import ValidationError


class PasswordChecker:
    @staticmethod
    def is_password_strong(password):
        # Check if password contains lowercase letters
        if not re.search(r"[a-z]+", password):
            return False

        # Check if password contains digits
        if not re.search(r"[0-9]+", password):
            return False

        # Check if password contains uppercase letters
        if not re.search(r"[A-Z]+", password):
            return False

        # Check if password contains special characters
        if not re.search(r"[!@#$%^&*()\-_=+{}[\]|\\:;\"'<>?,./]+", password):
            return False

        # Password satisfies all criteria
        return True

    @staticmethod
    def is_password_equals_re_password(password, re_password):
        return password == re_password

    @classmethod
    def password_serializer_validator(cls, password, re_password):
        # Check if password and re_password are the same
        if not cls.is_password_equals_re_password(password, re_password):
            raise ValidationError(
                "Please confirm that the re-entered password matches the original password"
            )

        # Check if password is strong
        if not cls.is_password_strong(password):
            raise ValidationError(
                "Password must contains lowercase, uppercase letters,special characters and digits"
            )
