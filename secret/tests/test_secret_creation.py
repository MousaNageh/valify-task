from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from secret.queryset.secret_queryset import SecretQueryset
from secret.tests.dataset import valid_secrets_string_dataset, not_exist_emails
from user.tests.dataset import user_valid_dataset


class CreateSecretAuthorization(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("secret-api")
        self.user1 = get_user_model().objects.create(
            **user_valid_dataset[0], is_active=True
        )
        self.user2 = get_user_model().objects.create(
            **user_valid_dataset[1], is_active=True
        )
        self.client.force_authenticate(user=self.user1)

    def test_create_secret_with_not_exist_emails(self):
        res = self.client.post(
            self.url,
            data={
                "secret": valid_secrets_string_dataset[0],
                "shared_with": not_exist_emails,
            },
            format="json",
        )
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        for email in not_exist_emails:
            self.assertIn(email, res.content.decode())

    def test_create_secret_with_not_valid_emails(self):
        res = self.client.post(
            self.url,
            data={
                "secret": valid_secrets_string_dataset[0],
                "shared_with": ["email1", "email2"],
            },
            format="json",
        )
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_create_secret(self):
        res = self.client.post(
            self.url,
            data={
                "secret": valid_secrets_string_dataset[0],
                "shared_with": [self.user2.email],
            },
            format="json",
        )
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertEqual(valid_secrets_string_dataset[0], res.data.get("secret"))
        get_res = self.client.get(self.url)
        for result in get_res.data.get("results"):
            for shared_with in result.get("shared_with"):
                self.assertEqual(self.user2.email, shared_with.get("user").get("email"))
                self.assertEqual(
                    self.user2.full_name, shared_with.get("user").get("full_name")
                )
