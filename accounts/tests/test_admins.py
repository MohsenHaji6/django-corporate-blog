from unittest.mock import Mock

from django.contrib import admin
from django.test import RequestFactory, TestCase

from accounts.admin import CustomUserAdmin
from accounts.models import CustomUser


class CustomUserAdminTest(TestCase):
    def test_shows_phone_number_if_has_not_name(self):
        user = CustomUser.objects.create_user(phone_number="09121111111")  # type: ignore
        admin_instance = CustomUserAdmin(CustomUser, admin.site)

        self.assertEqual(admin_instance.full_name(user), "09121111111")

    def test_shows_name_if_has_name(self):
        user = CustomUser.objects.create_user(
            phone_number="09121111111", first_name="Test", last_name="Case"
        )  # type: ignore

        admin_instance = CustomUserAdmin(CustomUser, admin.site)

        self.assertEqual(admin_instance.full_name(user), "Test Case")

    def test_save_model_on_change_mode(self):
        user = CustomUser.objects.create_user(
            phone_number="09121111111", password="UserPass"
        )  # type: ignore

        request = RequestFactory().get("/admin/")
        admin_instance = CustomUserAdmin(CustomUser, admin.site)

        form = Mock()
        admin_instance.save_model(request, user, form, change=True)

        self.assertTrue(user.check_password("UserPass"))

    def test_save_model_on_add_mode(self):
        user = CustomUser(phone_number="09121111111", password="UserPass")
        request = RequestFactory().get("/admin/")
        admin_instance = CustomUserAdmin(CustomUser, admin.site)

        form = Mock()
        admin_instance.save_model(request, user, form, change=False)

        self.assertTrue(user.check_password("UserPass"))
