from django.db import transaction
from secret.queryset.shared_secret_queryset import SharedSecretQueryset
from secret.models import Secret


class SecretQueryset:
    @staticmethod
    def get_user_secrets(user):
        return Secret.objects.prefetch_related(
            "shared_secrets", "shared_secrets__user"
        ).filter(user=user)

    @staticmethod
    def create_secret_with_shared_secrets(user, secret, shared_with_emails):
        with transaction.atomic():
            created_secret = Secret.objects.create(user=user, secret=secret)
            if shared_with_emails:
                SharedSecretQueryset.create_shared_secrets(
                    secret=created_secret, user_emails=shared_with_emails
                )
            return created_secret
