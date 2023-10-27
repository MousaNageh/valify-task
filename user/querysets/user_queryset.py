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
