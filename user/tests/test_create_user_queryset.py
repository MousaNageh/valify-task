from django.contrib.auth import get_user_model
from django.test import TestCase
from user.tests.dataset import user_valid_dataset, queryset_dataset


class UsersCreateTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**user_valid_dataset[0], is_active=True)
        self.assertEqual(user.email, user_valid_dataset[0]["email"])
        self.assertTrue(user.check_password(user_valid_dataset[0]["password"]))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(**user_valid_dataset[0])
        self.assertEqual(admin_user.email, user_valid_dataset[0]["email"])
        self.assertTrue(admin_user.check_password(user_valid_dataset[0]["password"]))
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

    def test_not_valid_inputs(self):
        User = get_user_model()
        for test_case in queryset_dataset.values():
            with self.assertRaises(ValueError):
                User.objects.create_user(**test_case)
