from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from user.querysets.user_queryset import UserQueryset
from secret.models import Secret, SharedSecret
from secret.tests.dataset import valid_secrets_string_dataset, not_exist_emails
from user.tests.dataset import user_valid_dataset


class CreateShareSecretWithUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("secret-share-with-api")
        self.user1 = UserQueryset.create_user(**user_valid_dataset[0], is_active=True)
        self.user2 = UserQueryset.create_user(**user_valid_dataset[1], is_active=True)
        self.client.force_authenticate(user=self.user1)
        self.secret = self._create_secret()

    def test_share_secret_with_empty_emails(self):
        res = self.client.post(
            self.url,
            data={"secret_id": self.secret.id, "shared_with": [],},
            format="json",
        )
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_share_secret_with_not_valid_emails(self):
        res = self.client.post(
            self.url,
            data={
                "secret_id": self.secret.id,
                "shared_with": ["email@", "email@email.com"],
            },
            format="json",
        )
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_share_secret_with_not_exist_secret(self):
        res = self.client.post(
            self.url,
            data={"secret_id": 12332, "shared_with": [self.user2.email], },
            format="json",
        )
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_share_secret_with_not_exist_emails(self):
        res = self.client.post(
            self.url,
            data={"secret_id": self.secret.id, "shared_with": not_exist_emails},
            format="json",
        )
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        for email in not_exist_emails:
            self.assertIn(email, res.content.decode())

    def test_share_secret_with_users_already_secret_shared_with_them(self):
        self._create_shared_secret()
        res = self.client.post(
            self.url,
            data={"secret_id": self.secret.id, "shared_with": [self.user2.email]},
            format="json",
        )
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn(self.user2.email, res.content.decode())

    def test_share_secret_with_users(self):
        res = self.client.post(
            self.url,
            data={"secret_id": self.secret.id, "shared_with": [self.user2.email],},
            format="json",
        )
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertIn(self.user2.email, res.data.get("shared_with"))

    def _create_shared_secret(self):
        SharedSecret.objects.create(secret=self.secret, user=self.user2)

    def _create_secret(self):
        return Secret.objects.create(
            user=self.user1, secret=valid_secrets_string_dataset[0]
        )
