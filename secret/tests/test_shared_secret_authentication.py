from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.status import HTTP_401_UNAUTHORIZED

from user.tests.dataset import user_valid_dataset


class SharedSecretAuthentication(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.get_url = reverse("shared-secret-list-api")
        self.encrypt_url = reverse("shared-secret-decrypt-api", args=[1])
        self.user = get_user_model().objects.create(
            **user_valid_dataset[0], is_active=True
        )

    def test_user_can_get_shared_secrets_without_login(self):
        res = self.client.get(self.get_url)
        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)

    def test_user_can_encrypt_shared_secrets_without_login(self):
        res = self.client.post(self.encrypt_url)
        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)
