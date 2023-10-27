from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK
from secret.queryset.secret_queryset import SecretQueryset
from secret.tests.dataset import valid_secrets_string_dataset
from user.tests.dataset import user_valid_dataset


class SecretAuthorization(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("secret-api")
        self.user1 = get_user_model().objects.create(
            **user_valid_dataset[0], is_active=True
        )
        self.user2 = get_user_model().objects.create(
            **user_valid_dataset[1], is_active=True
        )
        self._create_secrets()

    def test_user_can_get_secrets_of_anther_user(self):
        self.client.force_authenticate(user=self.user2)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertFalse(len(res.data.get("results")))

    def test_user_can_get_shared_secrets(self):
        self.client.force_authenticate(user=self.user1)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(
            len(valid_secrets_string_dataset), len(res.data.get("results"))
        )

    def _create_secrets(self):
        for secret in valid_secrets_string_dataset:
            SecretQueryset.create_secret_with_shared_secrets(
                user=self.user1, secret=secret, shared_with_emails=None
            )
