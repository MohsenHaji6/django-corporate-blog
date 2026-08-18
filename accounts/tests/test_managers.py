from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserManagerTest(TestCase):
    def assert_create_user_raises(self, phone_number, msg):
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_user(phone_number)  # type: ignore
        self.assertEqual(str(context.exception), msg)

    def test_create_user_if_empty_phone_number(self):
        self.assert_create_user_raises("", "The given phone number must be set")

    def test_create_user_if_not_str_phone_number(self):
        self.assert_create_user_raises(98912111111, "Phone number must be a string.")

    def test_create_user_with_password(self):

        user = get_user_model().objects.create_user(
            phone_number="09121111111", password="UserPass"
        )  # type: ignore
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password("UserPass"))

    def test_create_user_without_password(self):
        user = get_user_model().objects.create_user(phone_number="09122222222")  # type: ignore

        self.assertFalse(user.has_usable_password())

    def test_create_user_strips_phone_number(self):
        user = get_user_model().objects.create_user(phone_number=" 09121111111 ")  # type: ignore

        self.assertEqual(user.phone_number, "09121111111")

    def assert_create_superuser_raises(self, phone_number, password, msg, **extra_fields):
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_superuser(
                phone_number, password, **extra_fields
            )
        self.assertEqual(str(context.exception), msg)

    def test_create_superuser_if_not_password(self):
        self.assert_create_superuser_raises(
            "09121111111", "", "Superusers must have a password."
        )

    def test_create_superuser_if_is_staff_not_true(self):
        self.assert_create_superuser_raises(
            "09121111111", "UserPass", "Superuser must have is_staff=True.", is_staff=False
        )

    def test_create_superuser_if_is_superuser_not_true(self):
        self.assert_create_superuser_raises(
            "09121111111",
            "UserPass",
            "Superuser must have is_superuser=True.",
            is_superuser=False,
        )

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            phone_number="09121111111",
            password="UserPass",
        )  # type: ignore

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("UserPass"))
