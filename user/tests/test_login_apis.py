from django.test import TestCase
from user.querysets.user_queryset import UserQueryset
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.tests.dataset import user_valid_dataset


class APILoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("user-login")

    def test_login_with_valid_credentials(self):
        self.__create_user()
        res = self.client.post(self.url, user_valid_dataset[0])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        self.__create_user()
        res = self.client.post(self.url, user_valid_dataset[1])
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_invalid_password(self):
        self.__create_user()
        res = self.client.post(
            self.url, {"email": user_valid_dataset[0]["email"], "password": "foofoo"}
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_invalid_email(self):
        self.__create_user()
        res = self.client.post(
            self.url,
            {
                "email": user_valid_dataset[1]["email"],
                "password": user_valid_dataset[0]["password"],
            },
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def __create_user():
        UserQueryset.create_user(**user_valid_dataset[0], is_active=True)
