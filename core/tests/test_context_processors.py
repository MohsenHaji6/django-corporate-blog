from django.urls import reverse

from .base import BaseCoreTest


class ContextProcessorsTest(BaseCoreTest):
    def test_address_is_primary_and_is_active(self):
        self.create_address(is_primary=True, is_active=True)
        response = self.client.get(reverse("core:home"))
        address = response.context["address"]

        self.assertTrue(address.is_primary & address.is_active)

    def test_phone_is_primary_and_is_active(self):
        self.create_phone_number(is_primary=True, is_active=True)
        response = self.client.get(reverse("core:home"))
        phone = response.context["phone"]

        self.assertTrue(phone.is_primary & phone.is_active)
