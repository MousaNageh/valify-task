from rest_framework.exceptions import ValidationError

from secret.queryset.shared_secret_queryset import SharedSecretQueryset
from user.querysets.user_queryset import UserQueryset


class SharedSecretValidator:
    def __init__(self, user_emails: list, user):
        self._user_emails = self._get_unique_user_emails(user_emails)
        self._user = user
        self._validate_user_share_secret_with_himself()
        self._validate_all_user_emails_exist()

    def _validate_user_share_secret_with_himself(self):
        if self._user.email in self._user_emails:
            raise ValidationError("You cannot share the secret with yourself.")

    def _validate_all_user_emails_exist(self):
        existing_emails = UserQueryset.get_users_by_email(
            emails=self._user_emails, email_values_only=True
        )
        if len(existing_emails) != len(self._user_emails):
            not_exists_emails = [
                email for email in self._user_emails if email not in existing_emails
            ]
            raise ValidationError(f"Users with emails {not_exists_emails} not exists .")

    @property
    def validated_emails(self):
        return self._user_emails

    @classmethod
    def _get_unique_user_emails(cls, user_emails):
        return list(set(cls._get_normalized_emails(user_emails)))

    @staticmethod
    def _get_normalized_emails(user_emails):
        return [email.lower() for email in user_emails]
