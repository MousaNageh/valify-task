from django.contrib.auth.models import BaseUserManager
from user.querysets.user_queryset import UserQueryset
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    queryset = UserQueryset()

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError(_("The Email must be set"))

        if not password:
            raise ValueError(_("The Password must be set"))

        if not extra_fields.get("full_name"):
            raise ValueError(_("The full name must be set"))

        email = self.normalize_email(email).lower()

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new superuser"""
        extra_fields.update(
            {"is_staff": True, "is_superuser": True, "is_active": True, }
        )
        return self.queryset.create_user(email=email, password=password, **extra_fields)
