from django.contrib.auth import get_user_model


class UserQueryset:
    @staticmethod
    def create_user(email, password, **extra_fields):
        return get_user_model().objects.create_user(
            email=email, password=password, **extra_fields
        )

    @staticmethod
    def create_superuser(email, password, **extra_fields):
        return get_user_model().objects.create_superuser(
            email=email, password=password, **extra_fields
        )

    @staticmethod
    def get_users_by_email(emails, email_values_only=False):
        query = get_user_model().objects.filter(email__in=emails)
        if email_values_only:
            return query.values_list("email", flat=True)
        return query
