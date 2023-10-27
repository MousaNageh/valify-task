from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from .secret_model import Secret
from django.utils.translation import gettext_lazy as _


class SharedSecret(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name="user_shared_secrets",
        db_index=True,
        on_delete=models.CASCADE,
    )
    secret = models.ForeignKey(
        Secret, related_name="shared_secrets", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "secret")]
        verbose_name = _("Shared With")
        verbose_name_plural = _("Shared With")
