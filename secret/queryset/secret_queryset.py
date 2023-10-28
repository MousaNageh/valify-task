from django.db import transaction, models
from secret.queryset.shared_secret_queryset import SharedSecretQueryset
from secret.models import Secret, SharedSecret


class SecretQueryset:
    @staticmethod
    def get_user_secrets(user):
        return (
            Secret.objects.prefetch_related(
                models.Prefetch(
                    "shared_secrets", SharedSecret.objects.order_by("-created_at")
                ),
                "shared_secrets__user",
            )
            .filter(user=user)
            .order_by("-created_at")
        )

    @staticmethod
    def create_secret_with_shared_secrets(user, secret, shared_with_emails):
        with transaction.atomic():
            created_secret = Secret.objects.create(user=user, secret=secret)
            if shared_with_emails:
                SharedSecretQueryset.create_shared_secrets(
                    secret=created_secret, user_emails=shared_with_emails
                )
            return created_secret

    @staticmethod
    def get_secret_or_none(user, secret_id):
        try:
            return Secret.objects.get(id=secret_id, user=user)
        except Secret.DoesNotExist:
            return None
