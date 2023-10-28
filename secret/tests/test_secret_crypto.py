from django.test import TestCase
from secret.crypto.secret_crypto import SecretCrypto
from user.querysets.user_queryset import UserQueryset
from user.tests.dataset import user_valid_dataset
from secret.models import Secret


class SecretCryptoTests(TestCase):
    def setUp(self):
        self.user = UserQueryset.create_user(**user_valid_dataset[1], is_active=True)

        self.secret = "This is a secret"

    def test_encrypt_secret(self):
        encrypted_secret = SecretCrypto.encrypt_secret(self.secret)
        self.assertNotEqual(self.secret, encrypted_secret)

    def test_encrypted_secret_not_equal(self):
        encrypted_secret1 = SecretCrypto.encrypt_secret(self.secret)
        encrypted_secret2 = SecretCrypto.encrypt_secret(self.secret)
        self.assertNotEqual(encrypted_secret1, encrypted_secret2)

    def test_decrypt_secret(self):
        encrypted_secret = SecretCrypto.encrypt_secret(self.secret)
        decrypted_secret = SecretCrypto.decrypt_secret(encrypted_secret)
        self.assertEqual(self.secret, decrypted_secret)

    def test_save_decrypted_secret(self):
        secret_instance = Secret(user=self.user, secret=self.secret)
        secret_instance.save()
        self.assertEqual(
            self.secret, SecretCrypto.decrypt_secret(secret_instance.secret)
        )

    def test_save_encrypted_secret_not_equal(self):
        secret_instance = Secret(user=self.user, secret=self.secret)
        secret_instance.save()
        self.assertNotEqual(
            SecretCrypto.encrypt_secret(self.secret), secret_instance.secret
        )
