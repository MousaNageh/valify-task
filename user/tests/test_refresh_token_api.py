from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.tests.dataset import user_valid_dataset
import json


class APIRefreshTokenTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.client = APIClient()
        self.login_url = reverse("user-login")
        self.url = reverse("user-refresh-token")

    def test_get_new_access_with_valid_refresh_token(self):
        self.__create_user()
        res = self.client.post(self.login_url, user_valid_dataset[0])
        res_content = json.loads(res.content)
        refresh = res_content.get("refresh")
        res = self.client.post(self.url, {"refresh": refresh})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_new_access_with_invalid_refresh_token(self):
        self.__create_user()
        res = self.client.post(self.login_url, user_valid_dataset[0])
        res_content = json.loads(res.content)
        refresh = res_content.get("access")
        res = self.client.post(self.url, {"refresh": refresh})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def __create_user(self):
        self.User.objects.create_user(**user_valid_dataset[0], is_active=True)
