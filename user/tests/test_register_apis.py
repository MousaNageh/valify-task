from django.test import TestCase
from rest_framework import status

from django.urls import reverse
from rest_framework.test import APIClient
from user.tests.dataset import register_dataset


class APIRegisterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("user-register")

    def test_register_weak_password(self):
        res = self.client.post(self.url, register_dataset.get("weak_password"))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_password(self):
        res = self.client.post(self.url, register_dataset.get("empty_password"))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_not_equal_passwords_passwords(self):
        res = self.client.post(
            self.url, register_dataset.get("not_equal_passwords_passwords")
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_not_valid_email(self):
        res = self.client.post(self.url, register_dataset.get("not_valid_email"))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_email(self):
        res = self.client.post(self.url, register_dataset.get("empty_email"))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_full_name(self):
        res = self.client.post(self.url, register_dataset.get("empty_full_name"))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_valid_data(self):
        res = self.client.post(self.url, register_dataset.get("valid_data"))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            register_dataset.get("valid_data").get("email"), res.data.get("email")
        )
        self.assertEqual(
            register_dataset.get("valid_data").get("full_name"),
            res.data.get("full_name"),
        )
