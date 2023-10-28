from secret.models import SharedSecret
from user.querysets.user_queryset import UserQueryset


class SharedSecretQueryset:
    @staticmethod
    def get_shared_secret_for_users(user_emails: list, select_user=True):
        query = SharedSecret.objects.filter(user__email__in=user_emails)
        if select_user:
            return query.select_related("user")
        return query

    @staticmethod
    def get_shared_secret_for_users_by_secret(
        user_emails: list, secret, emails_only=True
    ):
        query = SharedSecret.objects.filter(user__email__in=user_emails, secret=secret)
        if emails_only:
            return query.select_related("user").values_list("user__email", flat=True)
        return query

    @staticmethod
    def create_shared_secrets(secret, user_emails):
        users = UserQueryset.get_users_by_email(user_emails)
        shared_secrets = [SharedSecret(user=user, secret=secret) for user in users]
        SharedSecret.objects.bulk_create(shared_secrets, batch_size=500)

    @staticmethod
    def get_shared_secrets_for_user(user):
        return SharedSecret.objects.select_related("secret", "secret__user").filter(
            user=user
        )

    @staticmethod
    def get_shared_secret_by_id_and_user(user, shared_secret_id):
        try:
            return SharedSecret.objects.select_related("secret").get(
                id=shared_secret_id, user=user,
            )
        except SharedSecret.DoesNotExist:
            return None
