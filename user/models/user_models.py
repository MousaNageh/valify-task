from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from user.manager.user_manager import UserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return self.email
