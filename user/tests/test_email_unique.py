from django.contrib.auth import get_user_model
from django.test import TestCase
from user.tests.dataset import user_valid_dataset
from django.db import IntegrityError


class EmailUnique(TestCase):
    def test_unique_email(self):
        User = get_user_model()
        User.objects.create_user(**user_valid_dataset[0], is_active=True)
        # IntegrityError will be raised if email is exists
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**user_valid_dataset[0], is_active=True)
