from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

from secret.crypto.secret_crypto import SecretCrypto
from django.db import models


class Secret(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name="user_secrets",
        db_index=True,
        on_delete=models.CASCADE,
    )
    secret = models.TextField(validators=[MinLengthValidator(8)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.secret

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.pk:
            self.secret = SecretCrypto.encrypt_secret(self.secret)
        super().save(force_insert, force_update, using, update_fields)
