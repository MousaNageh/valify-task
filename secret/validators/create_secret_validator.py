from rest_framework.exceptions import ValidationError

from secret.queryset.secret_queryset import SecretQueryset
from secret.queryset.shared_secret_queryset import SharedSecretQueryset
from user.querysets.user_queryset import UserQueryset


class SharedSecretValidator:
    def __init__(self, user_emails: list, user, secret_id=None):
        self._user_emails = self._get_unique_user_emails(user_emails)
        self._user = user
        self._secret = None
        self._validate_user_can_not_share_secret_with_himself()
        self._validate_all_user_emails_are_exist()
        if secret_id:
            self._validate_user_already_secret_shared_with_them(secret_id)

    def _validate_user_can_not_share_secret_with_himself(self):
        print(self._user.email)
        if self._user.email in self._user_emails:
            raise ValidationError("You cannot share the secret with yourself.")

    def _validate_all_user_emails_are_exist(self):
        existing_emails = UserQueryset.get_users_by_email(
            emails=self._user_emails, email_values_only=True
        )
        if len(existing_emails) != len(self._user_emails):
            not_exists_emails = [
                email for email in self._user_emails if email not in existing_emails
            ]
            raise ValidationError(f"Users with emails {not_exists_emails} not exists .")

    def _validate_user_already_secret_shared_with_them(self, secret_id):
        secret = self._get_secret_or_raise_error(secret_id)
        shared_emails = SharedSecretQueryset.get_shared_secret_for_users_by_secret(
            user_emails=self._user_emails, secret=secret
        )
        already_shared_emails = [email for email in shared_emails]
        if already_shared_emails:
            raise ValidationError(
                f"Users with emails {already_shared_emails} secret already shared with them."
            )

    def _get_secret_or_raise_error(self, secret_id):
        secret = SecretQueryset.get_secret_or_none(user=self._user, secret_id=secret_id)
        if not secret:
            raise ValidationError(f"secret with id {secret_id} not exists .")
        self._secret = secret
        return secret

    @property
    def validated_emails(self):
        return self._user_emails

    @property
    def secret(self):
        return self._secret

    @classmethod
    def _get_unique_user_emails(cls, user_emails):
        return list(set(cls._get_normalized_emails(user_emails)))

    @staticmethod
    def _get_normalized_emails(user_emails):
        return [email.lower() for email in user_emails]
