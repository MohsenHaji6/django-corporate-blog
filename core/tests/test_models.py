from django.db import IntegrityError

from core.models import SiteSetting
from core.tests.base import BaseCoreTest


class SiteSettingTest(BaseCoreTest):
    def test_save_only_one_record_in_site_setting_model(self):
        site_setting = SiteSetting()
        site_setting.site_title = "test site title 2"
        site_setting.save()
        self.assertEqual(SiteSetting.objects.count(), 1)
        self.assertEqual(site_setting.site_title, "test site title 2")


class PhoneNumberTest(BaseCoreTest):
    def test_one_phone_number_can_be_primary(self):
        self.create_phone_number(is_primary=True)

        with self.assertRaises(IntegrityError):
            self.create_phone_number(use_for="for test2", is_primary=True)

    def test_unique_use_for_phone_number(self):
        self.create_phone_number()

        with self.assertRaises(IntegrityError):
            self.create_phone_number()


class AddressTest(BaseCoreTest):
    def test_one_address_can_be_primary(self):
        self.create_address(is_primary=True)

        with self.assertRaises(IntegrityError):
            self.create_address(is_primary=True)
