from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from secret.queryset.secret_queryset import SecretQueryset
from secret.tests.dataset import valid_secrets_string_dataset
from secret.models import SharedSecret
from user.querysets.user_queryset import UserQueryset
from user.tests.dataset import user_valid_dataset


class SharedSecretAuthorization(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.get_url = reverse("shared-secret-list-api")

        self.user1 = UserQueryset.create_user(**user_valid_dataset[0], is_active=True)
        self.user2 = UserQueryset.create_user(**user_valid_dataset[1], is_active=True)
        self._create_secrets()

    def test_user_can_get_shared_secrets_of_anther_user(self):
        self.client.force_authenticate(user=self.user1)
        res = self.client.get(self.get_url)
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertFalse(len(res.data.get("results")))

    def test_user_can_encrypt_shared_secrets_of_anther_user(self):
        self.client.force_authenticate(user=self.user1)
        res = self.client.get(
            reverse("shared-secret-decrypt-api", args=[self._get_id_of_shared_secret()])
        )
        self.assertEqual(res.status_code, HTTP_404_NOT_FOUND)

    def test_user_can_get_shared_secrets(self):
        self.client.force_authenticate(user=self.user2)
        res = self.client.get(self.get_url)
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(
            len(valid_secrets_string_dataset), len(res.data.get("results"))
        )

    def _create_secrets(self):
        for secret in valid_secrets_string_dataset:
            SecretQueryset.create_secret_with_shared_secrets(
                user=self.user1, secret=secret, shared_with_emails=[self.user2.email]
            )

    def _get_id_of_shared_secret(self):
        return SharedSecret.objects.filter(user=self.user2).first().id
